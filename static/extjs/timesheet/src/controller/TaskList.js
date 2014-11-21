Ext.define('Ext.calendar.controller.TaskListController', {
    extend: 'Ext.app.Controller',
	stores: ['Tasks'],
	models: ['Task'],
	views: [
        'TaskList'
    ],
        
	init: function() {
        this.control({
            'viewport > tasklist': {
                render: this.onPanelRendered
            }
        });
        console.log('The panel was rendered');
    },

    onPanelRendered: function() {
        console.log('The panel was rendered');
    }
    },
    
    selectEvent: function(grid, record) {
    	/*
		var view = Ext.widget('useredit');
        view.down('form').loadRecord(record);
        */
        console.log('Grid item clicked');
        
	}
	
    /*,
	
	updateUser: function(button) {
        console.log('clicked the Save button');
		var win    = button.up('window'),
        	form   = win.down('form'),
        	record = form.getRecord(),
        	values = form.getValues();

		record.set(values);
		win.close();
    },

	

	onPanelRendered: function() {
        console.log('The panel was rendered');
    }*/
});
