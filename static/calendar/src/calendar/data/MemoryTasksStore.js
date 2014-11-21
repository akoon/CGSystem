//获取当前用户Id
//console.log('user-id      ' + Ext.get("user-id").dom.innerHTML);

Ext.define('Extensible.calendar.data.MemoryTasksStore', {
    extend: 'Ext.data.Store',
    model: 'Extensible.calendar.data.TaskModel',
	autoLoad: true,
	remoteFilter : true,
	proxy: {
		type: 'ajax',
		api: {
				read: '/get_user_tasks/' + Ext.get("user-id").dom.innerHTML
		},
		reader: {
				type: 'json',
				root: 'tasks',
				successProperty: 'success'
		}
	}
});
