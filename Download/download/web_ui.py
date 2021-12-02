from datetime import datetime
import os
import shutil
import unicodedata

from trac.env import Environment
from trac.core import (
    Component,
    implements,
    ExtensionPoint,
    Interface,
    TracError
)
from trac.util.html import html
from trac.admin.api import IAdminPanelProvider
from trac.web import IRequestHandler
from trac.perm import IPermissionRequestor
from trac.web.chrome import (
    INavigationContributor,
    add_notice,
    add_warning
)

from trac.config import BoolOption, IntOption, ListOption, Option, PathOption
from trac.resource import Resource
from trac.mimeview import Mimeview
from trac.util.datefmt import format_datetime, to_timestamp, utc
from trac.util.text import to_unicode


class Download(Component):

    implements(INavigationContributor, IRequestHandler,
               IAdminPanelProvider, IPermissionRequestor)

    path = PathOption(
               'download',
               'path',
               '../download',
               doc='Path where to store uploaded downloads.'
           )

    ext = ListOption(
              'download',
              'ext',
              'zip,gz,bz2,rar',
              doc="List of file extensions allowed to upload. Set to 'all'"
                  "to specify that any file extensions is allowed."
          )

    max_size = IntOption(
                   'download',
                   'max_size',
                   268697600,
                   'Maximum allowed file size (in bytes) for downloads. Default'
                   'is 256 MB.'
               )

    # INavigationContributor methods

    def get_active_navigation_item(self, req):
        return 'download'

    def get_navigation_items(self, req):
        if 'DOWNLOAD_VIEW' in req.perm('download'):
            yield (
                'mainnav',
                'download', 
                html.a('Download', href=req.href.download())
            )

    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info.find('/download') == 0

    def process_request(self, req):
        data = {}
        self.do_action(req)
        cursor = self.env.db_query(
                     'SELECT id, year, file, description FROM download ORDER BY id'
                 )
        data['downloads'] = [(row[0], row[1], row[2], row[3]) for row in cursor]
        return 'download_list.html', data, {}

    # IAdminPageProvider methods
    def get_admin_panels(self, req):
        if 'DOWNLOAD_ADMIN' in req.perm('download'):
            yield 'download', 'Download', 'settings', 'Settings'

    def render_admin_panel(self, req,  cat, page, version):
        # here comes the page content, handling, etc.
        data = {}
        self.do_action(req)
        cursor = self.env.db_query(
                     'SELECT id, year, file, description, size, time, author '
                     'FROM download ORDER BY id'
                 )
        data['downloads'] = [(row[0], row[1], row[2], row[3]) for row in cursor]
        return 'download_admin.html', data, {}

    # IPermissionRequestor methods.
    def get_permission_actions(self):
        view = 'DOWNLOAD_VIEW'
        add = ('DOWNLOAD_ADD', ['DOWNLOAD_VIEW'])
        admin = ('DOWNLOAD_ADMIN', ['DOWNLOAD_VIEW', 'DOWNLOAD_ADD'])
        return [view, add, admin]

    def get_download_id_by_time(self, time):
        cursor = self.env.db_query(
                     'SELECT id, file, description, size, time, author '
                     'FROM download where time={}'.format(time)
                 )
        for row in cursor:
            return row[0]
        return {}

    def get_file_from_req(self, req):
        file = req.args['file']

        # Test if file is uploaded.
        if not hasattr(file, 'filename') or not file.filename:
            raise TracError('No file uploaded.')

        # Get file size.
        if hasattr(file.file, 'fileno'):
            size = os.fstat(file.file.fileno())[6]
        else:
            # Seek to end of file to get its size.
            file.file.seek(0, 2)
            size = file.file.tell()
            file.file.seek(0)
        if size == 0:
            raise TracError("Can't upload empty file.")

        # Try to normalize the filename to unicode NFC if we can.
        # Files uploaded from OS X might be in NFD.
        self.log.debug('input filename: %s', file.filename)
        filename = unicodedata.normalize(
                       'NFC',
                       to_unicode(file.filename, 'utf-8')
                   )
        filename = filename.replace('\\', '/').replace(':', '/')
        filename = os.path.basename(filename)
        self.log.debug('output filename: %s', filename)

        return file.file, filename, size

    def add_download(self, download, file):
        # Check for maximum file size.
        if 0 <= self.max_size < download['size']:
            raise TracError(
                'Maximum file size: %s bytes' % self.max_size,
                'Upload failed'
            )

        # Add new download to DB.
        now = datetime.now()
        sql = 'INSERT INTO download (year,file,description,size,time,author) VALUES(year(curdate()),%s,%s,%s,%s,%s)'
        args = (download['file'], download['description'],
                download['size'], download['time'], download['author'])
        self.env.db_transaction(sql, args)
        self.log.debug("FileUpload SQL: %s", sql)

        # Get inserted download by time to get its ID.
        id = self.get_download_id_by_time(download['time'])
        self.log.debug('FileUpload id: %s', id)

        # Prepare file paths.
        path = os.path.normpath(os.path.join('/var/www/trac/download',str(now.year)))
        filepath = os.path.normpath(os.path.join(path, download['file']))
        self.log.debug('FileUpload path: %s', path)
        self.log.debug('FileUpload filepath: %s', filepath)

        # Store uploaded image.
        try:            
            if not os.path.isdir(path):
                os.mkdir(path.encode('utf-8'))		
            if os.path.exists(filepath):
                remove(filepath)				
            with open(filepath.encode('utf-8'), 'wb+') as fileobj:
                file.seek(0)
                shutil.copyfileobj(file, fileobj)
        except Exception as error:
            self.log.debug(error)
            try:
                os.remove(filepath.encode('utf-8'))
            except:
                pass
            try:
                os.rmdir(path.encode('utf-8'))
            except:
                pass
            raise TracError(
                "Error storing file %s. Does the directory "
                "specified in path config option of [downloads] "
                "section of trac.ini exist?" % download['file']
            )

    def do_action(self, req):
        if req.method == "POST":
            submit = req.args.get('submit').strip()
            if submit == 'Add':
                # Get form values.
                file, filename, file_size = self.get_file_from_req(req)
                download = {
                    'file': filename,
                    'description': req.args.get('description'),
                    'size': file_size,
                    'time': to_timestamp(datetime.now(utc)),
                    'count': 0,
                    'author': req.authname
                }
                self.log.debug("FileUpload filename:" + download['file'])
                self.log.debug(
                    "FileUpload description:" + download['description']
                )
                self.log.debug("FileUpload size:", download['size'])
                self.log.debug("FileUpload time:", download['time'])
                self.log.debug("FileUpload author:" + download['author'])
                # Upload file to DB and file storage.
                self.add_download(download, file)
                file.close()

                add_notice(req, 'Download has been added.')
            elif submit == 'Remove':
                ids = req.args.getlist('sels')
                if ids is not None and len(ids) > 0:
                    for id in ids:
                        sql = "DELETE FROM download WHERE id ={}".format(
                            int(id))
                        self.env.db_transaction(sql)
                    add_notice(req, 'Download has been deleted.')
        else:
            # Get download.
            download_id = req.args.get('sel') or 0
            if int(download_id) > 0:
                sql = 'SELECT file, description, year FROM download where id={}'
                sql = sql.format(download_id)
                cursor = self.env.db_query(sql)
                if len(cursor) > 0:
                    fn = cursor[0][0]
                    description = cursor[0][1]
                    year = cursor[0][2]
                else:
                    raise TracError("File not found.")

                # Get download file path.
                filename = os.path.basename(fn)
                filepath = os.path.join(
                               self.path,
                               to_unicode(year),
                               filename
                           )
                filepath = os.path.normpath(filepath)

                # Increase downloads count.
                sql = 'UPDATE download SET count=count+1 WHERE id ={}'
                sql = sql.format(download_id)
                self.env.db_transaction(sql)

                # Guess mime type.
                with open(filepath.encode('utf-8'), 'r') as fileobj:
                    file_data = fileobj.read(1000)
                mimeview = Mimeview(self.env)
                mime_type = mimeview.get_mimetype(filepath, file_data)
                if not mime_type:
                    mime_type = 'application/octet-stream'
                if 'charset=' not in mime_type:
                    charset = mimeview.get_charset(file_data, mime_type)
                    mime_type = mime_type + '; charset=' + charset

                # Return uploaded file to request.
                req.send_header(
                    'Content-Disposition',
                    'attachment;filename="%s"' % os.path.normpath(fn)
                )
                req.send_header('Content-Description', description)
                req.send_file(filepath.encode('utf-8'), mime_type)
