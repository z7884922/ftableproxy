function obj2string(o){
	var r=[];
	if(typeof o=="string"){
		return "\""+o.replace(/([\'\"\\])/g,"\\$1").replace(/(\n)/g,"\\n").replace(/(\r)/g,"\\r").replace(/(\t)/g,"\\t")+"\"";
	}
	if(typeof o=="object"){
		if(!o.sort){
			for(var i in o){
				r.push(i+":"+obj2string(o[i]));
			}
			if(!!document.all&&!/^\n?function\s*toString\(\)\s*\{\n?\s*\[native code\]\n?\s*\}\n?\s*$/.test(o.toString)){
				r.push("toString:"+o.toString.toString());
			}
			r="{"+r.join()+"}";
		}else{
			for(var i=0;i<o.length;i++){
				r.push(obj2string(o[i]))
			}
			r="["+r.join()+"]";
		} 
		return r;
	} 
	return o.toString();
}

function render_ui(){
    insert_menu_markup();
    insert_grid_markup();
   // make_grid_component();
    //add_newtab_button();
    //insert_open_dialog_markup();
    //make_open_dialog();
    add_grid()
}

var tab_name='eventTable';

var loader = null;
var newRow={}
function insert_grid_markup(){
    var workbook_widget = '<div id="tabs"><ul><li></li></ul></div>';  
    $('body').append(workbook_widget);
    $('<div id="'+tab_name+'"></div>').appendTo('#tabs');
    $("#tabs").tabs("add","#" + tab_name,"Sheet " + 0, 0);
  
    $('#'+tab_name ).css('height','200');
    $('#'+tab_name ).css('width','820');
    $('#'+tab_name ).css('float','left');
}
				
// OK, it's not really a menu...yet :-)
function insert_menu_markup(){
    $("body").prepend('<input id="addrow" type="button" value="添加"/>');
    $("body").prepend('<input id="delrow" type="button" value="删除"/>');
    $("#addrow").click(function() {
	var dd = grid.getData();
	alert(newRow);
	dd.splice(dd.length,0,{"title":""});
	grid.invalidateRow(data.length);
	grid.updateRowCount();
	grid.render();
	grid.scrollRowIntoView(dd.length-1)
    });

    $("#delrow").click(function() {
	var dd = grid.getData();
	var current_row = grid.getActiveCell().row;
	dd.splice(current_row,1);
	var r = current_row;
	while (r<dd.length){
	    grid.invalidateRow(r);
	    r++;
	}
	grid.updateRowCount();
	grid.render();
	grid.scrollRowIntoView(current_row-1)
    });
}



//a dict from index to an dict

var grid;
//var loader = new Slick.Data.RemoteModel('http://localhost:9000/index.html');
//var loader = new Slick.Data.RemoteModel();

function add_grid(){
    loader = new Slick.Data.RemoteModel('http://localhost:9000/index.html');
    var current_cell = null;

    // column definitions
    var columns = [
        {id:"row", name:"#", field:"num", width:50, 
         cannotTriggerInsert:true, resizable:false, unselectable:true },
        {id:"tID", name:"table id", field:"tID", width:100, 
         editor: Slick.Editors.Text},
        {id:"client_id", name:"client id", field:"client_id", width:200, 
         editor: Slick.Editors.Text},
        {id:"secret", name:"secret", field:"secret", width:200, 
              editor: Slick.Editors.Text},
        {id:"redirect_uri", name:"redirect uri", field:"redirect_uri", width:250,
         editor: Slick.Editors.Text},
    ];

    var options = {
        editable: true,
        autoEdit: true,
        enableAddRow: true,
	AddRow: true,
        enableCellNavigation: true,
        enableCellRangeSelection : true,
        asyncEditorLoading: true,
        multiSelect: true,
        leaveSpaceForNewRows : true,
        rerenderOnResize : true,
	forceFitColumns: true
    };

    /*
    for( var i=0; i < 100 ; i++ ){
        var d = (workbook[i] = {});
        d["num"] = i;
        d["value"] = "";
    }
    */
    grid = new Slick.Grid($("#"+tab_name),loader.data, columns, options);

    
    grid.onCellChange.subscribe(function(e, args){
        d = grid.getData();
        row  = grid.getActiveCell().row;
	if (row >= d.length){
	    return;
	}
        cell = grid.getActiveCell().cell;
        //this_cell_data = d[row][grid.getColumns()[cell].field];
    });

    grid.onBeforeCellEditorDestroy.subscribe(function(e, args){
	//alert(obj2string(grid.getActiveCell()));
	//alert(obj2string(args));
        d = grid.getData();
        row  = grid.getActiveCell().row;
	cell = grid.getActiveCell().cell;
	if (row >= d.length){
	   // newRow[grid.getColumns()[cell].field]=d[row][grid.getColumns()[cell].field];
	    return;
	}

        this_cell_data = d[row][grid.getColumns()[cell].field];
    });
   

    grid.onAddNewRow.subscribe(function(e, args) {
	//TODO push data to server
	var item = args.item;
	data = grid.getData();
	grid.invalidateRow(data.length);
	//data.push(item);
	data[data.length]=item
	data.length=data.length+1;
	grid.render();
    })
     /**/
};

$('#save').on('click',function(){
    // Do a foreach on all the grids. The ^= operator gets all
    // the inputs with a name attribute that begins with data
    $("[name^='data']").each(function(index, value){
        var data_index = "data"+index;
        var sheet_id = $('#tabs_'+index+'_form').find('#sheet_id').val();
        if(sheet_id !== ''){
          sheet_id = eval(sheet_id);
        }

        // convenience variable for readability
        var data2post  = $.JSON.encode(workbook[data_index]);
        $("#"+data_index).val(data2post);

        $.post( '{% url index %}', {'app_action':'save', 'sheet_id': sheet_id,
                'workbook_name':$('#workbook_name').val(),
                'sheet':data_index, 'json_data':data2post});
    });
});


function load_tablemeta(){
    var loadingIndicator = null;
    grid.onViewportChanged.subscribe(function (e, args) {
	var vp = grid.getViewport();
	loader.ensureData(vp.top, vp.bottom);
    });
    
    loader.onDataLoading.subscribe(function () {
      if (!loadingIndicator) {
        loadingIndicator = $("<span class='loading-indicator'><label>Buffering...</label></span>").appendTo(document.body);
        var $g = $("#"+tab_name);

        loadingIndicator
            .css("position", "absolute")
            .css("top", $g.position().top + $g.height() / 2 - loadingIndicator.height() / 2)
            .css("left", $g.position().left + $g.width() / 2 - loadingIndicator.width() / 2);
      }

      loadingIndicator.show();
    });

    loader.onDataLoaded.subscribe(function (e, args) {
	for (var i = args.from; i <= args.to; i++) {
            grid.invalidateRow(i);
	}
	grid.updateRowCount();
	grid.render();

	loadingIndicator.fadeOut();
    });
    grid.onViewportChanged.notify();
/*  $('#tabs').load('{% url index.html %}', //the url to query
			     {'app_action':'get_sheets'},  // the data to send
			     function(sheet, resp, t){    //handling the response
				 sheet = $.JSON.decode(sheet);
				 alert("data recieved:"+sheet)
				 workbook = {}; // reset
				 //we have only one sheet
  
				 
				 // By calling eval, we translate value from
				 // a string to a JavaScript object
				 workbook = eval(value["data"]);

				 // insert data into hidden
				 $("#data").attr('value', workbook);
				 grid.setData(workbook);
				 grid.render();
			     });
*/
};

$('#open').on('click',function(){
    // load is used for doing asynchronous loading of data
    $('#workbook_list').load('index.html', {'app_action':'list'}, 
        function(workbooks,success){
        workbooks = $.JSON.decode(workbooks);
        $.each(workbooks, function(index, value){
            $('#workbook_list').append(
              '<option value="'+ value +'">'+value +'*lt;/option>');
        });
    });

    $('#dialog_form').dialog('open');
});

$(document).ready(function(){
    render_ui();
    load_tablemeta();
});