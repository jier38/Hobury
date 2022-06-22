# -*- coding: utf-8 -*-

from trac.util.html import html
from trac.util.text import pretty_size
from trac.wiki.macros import WikiMacroBase
from trac.web.api import IRequestFilter
from trac.core import implements
from trac.web.chrome import add_script, add_stylesheet

class ChartMacro(WikiMacroBase):
    implements(IRequestFilter)
	
	# [[Chart(TicketStatistics)]]
    def expand_macro(self, formatter, name, content):
        chart_type = ""
        buf = ""
        if content:
            argv = [arg.strip() for arg in content.split(',')]
            if len(argv) > 0:
                chart_type = argv[0]
				
        if (chart_type == 'TicketStatistics'):
            cursor = self.env.db_query(
                "SELECT t.milestone, (SELECT count(*) from ticket where milestone=t.milestone and status<>'closed') as open, (SELECT count(*) from ticket where milestone=t.milestone and status='closed') as closed from ticket t where milestone is not null group by milestone order by milestone;"
            )
            opentickets = ""
            closedtickets = ""
            ticks = ""
            for row in cursor:
                opentickets += str(row[1]) + ',' 
                closedtickets += str(row[2]) + ',' 
                tick = row[0].split(' ')
                ticks += '"' + tick[len(tick)-1] + '",' 
            #buf += '<div id="ticketschart" style="width: 500px; height: 300px;"></div>\n'
            #buf += '<script type="text/javascript">\n'
            #buf += '$(document).ready(function() { \n' 
            #buf +=     '  var opentickets = [' + opentickets + ']; \n' 
            #buf +=    '  var closedtickets = [' + closedtickets + ']; \n' 
            #buf +=    '  var ticks = [' + ticks + ']; \n'  		 
            #buf +=    '  var ticketsplot = $.jqplot("ticketschart", [opentickets, closedtickets], { \n' 
            #buf +=   '    series: [{label: "Open", renderer:$.jqplot.BarRenderer}, {label: "Closed", xaxis: "xaxis", yaxis: "yaxis"}], \n' 
            #buf +=    '    title: "Tickets per milestone", \n' 
            #buf +=     '    highlighter: {show: true}, grid: {background: "#fff"}, \n' 
            #buf +=      '    axesDefaults: {tickRenderer: $.jqplot.CanvasAxisTickRenderer}, \n' 
            #buf +=        '    axes: {xaxis: {renderer: $.jqplot.CategoryAxisRenderer, ticks: ticks, tickOptions: {showGridline: false}}, yaxis: {autoscale: true}}, \n' 
            #buf +=    '    legend: {show: true, location: "e", placement: "outside"} \n' 
            #buf +=      '  }); \n' 
            #buf +=     '}); \n'
            #buf += '</script>\n'
            buf += '<div id="ticketschart" style="width: 800px; height: 500px;"></div> \n'
            buf += '<script type="text/javascript"> \n'         
            buf += 'CHART = document.getElementById("ticketschart"); \n'
            buf += 'var trace1 = { \n'
            buf += '  x: [' + ticks + '], \n'
            buf += '  y: [' + opentickets + '], \n'
            buf += '  type: "bar", \n'
            buf += '  name: "Open", \n'
            buf += '}; \n'
            buf += 'var trace2 = { \n'
            buf += '  x: [' + ticks + '], \n'
            buf += '  y: [' + closedtickets + '], \n'
            buf += '  mode: "lines+markers", \n'
            buf += '  name: "Closed", \n'
            buf += '  marker: { size: 8 }, \n'
            buf += '  line: { width: 0.8 } \n'
            buf += '}; \n'
            buf += 'var data = [ trace1, trace2 ]; \n'
            buf += 'var layout = { title:"Tickets per milestone" }; \n'
            buf += 'Plotly.newPlot(CHART, data, layout); \n'
            buf += '</script> \n'








        elif (chart_type == 'Statistics'):
            cursor = self.env.db_query(
                "SELECT exchange, indicator, k, lambda, weightfunction, mRS_buy, mRS_sell, holdingperiod, rel_profit, win_ratio from invest.statistics;"
            )            
            buf += '<div id="output" style="margin: 10px;"></div>\n'
            buf += '<div id="plot" style="margin: 10px;"></div>\n'
            buf += '<script type="text/javascript">\n'
            buf += '    var csv = "exchange,indicator,k,lambda,weightfunction,mRS_buy,mRS_sell,holdingperiod,rel_profit,win_ratio\\n";\n'
            for row in cursor:
                buf += '    csv += "{},{},{},{},{},{},{},{},{},{}\\n";\n'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
            buf += '    $("#output").pivotUI(\n'
            buf += '       $.csv.toArrays(csv), { \n'
            buf += '          rows: ["weightfunction", "exchange", "lambda"],\n'
            buf += '          cols: ["k"],\n'
            buf += '          vals: ["rel_profit"],\n'
            buf += '          aggregatorName: "Average",\n'
            buf += '          rendererName: "Heatmap",\n'
            buf += '          renderers: $.extend($.pivotUtilities.renderers, $.pivotUtilities.plotly_renderers)\n'
            buf += '       }\n'
            buf += '    );\n'
            buf += '</script>\n'
        return buf
		
    def _has_perm(self, parent_realm, parent_id, filename, context):       
        return true

    # IRequestFilter#pre_process_request
    def pre_process_request(self, req, handler):
        return handler
		
    # IRequestFilter#post_process_request
    def post_process_request(self, req, template, data, content_type):
        #plugin_base = 'https://cdnjs.cloudflare.com/ajax/libs/jqPlot/1.0.9/'
        #add_script(req, plugin_base + 'jquery.jqplot.min.js')
        #add_script(req, plugin_base + 'plugins/jqplot.dateAxisRenderer.js')
        #add_script(req, plugin_base + 'plugins/jqplot.canvasTextRenderer.js')
        #add_script(req, plugin_base + 'plugins/jqplot.canvasAxisTickRenderer.js')
        #add_script(req, plugin_base + 'plugins/jqplot.categoryAxisRenderer.js')
        #add_script(req, plugin_base + 'plugins/jqplot.barRenderer.js')
        #add_script(req, plugin_base + 'plugins/jqplot.highlighter.min.js')
        #add_stylesheet(req, 'https://cdnjs.cloudflare.com/ajax/libs/jqPlot/1.0.9/jquery.jqplot.min.css')
        	
        add_script(req, 'https://cdnjs.cloudflare.com/ajax/libs/jquery-csv/1.0.5/jquery.csv.js')
        add_script(req, 'https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.js')
        add_script(req, 'https://cdn.plot.ly/plotly-basic-latest.min.js')
        add_script(req, 'https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/plotly_renderers.min.js')
        add_script(req, 'https://d3js.org/d3.v5.min.js')
        add_stylesheet(req, 'https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.css')
        add_script(req, 'https://cdn.plot.ly/plotly-2.9.0.min.js')
        return (template, data, content_type)		