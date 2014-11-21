Ext.define('Ext.calendar.data.CurrentUserStore', {
    extend: 'Ext.data.Store',
    model: 'Ext.calendar.data.UserModel',
	autoLoad: true,
	/*获取当前登录用户*/
	proxy: {
		type: 'ajax',
		api: {
				read: '/get_task_names',
		},
		reader: {
				type: 'json',
				root: 'user',
				successProperty: 'success'
		}
	}
});
