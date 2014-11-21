Ext.define('Ext.calendar.data.TaskListStore', {
    extend: 'Ext.data.Store',
    model: 'Ext.calendar.data.TaskModel',
	autoLoad: true,
	proxy: {
		type: 'ajax',
		//url: '/get_actual_tasks',
		url: '/get_user_tasks',
		reader: {
				type: 'json',
				root: 'tasks',
				successProperty: 'success'
		},
		method: 'GET'
	}
});
