Ext.define('Ext.calendar.store.TasksStore', {
    extend: 'Ext.data.Store',
    model: 'Ext.calendar.model.Task',
	autoLoad: true,
	
	proxy: {
		type: 'ajax',
		api: {
				read: '/get_task_names',
		},
		reader: {
				type: 'json',
				root: 'tasks',
				successProperty: 'success'
		}
	}
});
