//获取当前用户Id
//console.log('user-id      ' + Ext.get("user-id").dom.innerHTML);

Ext.define('Extensible.calendar.data.MemoryDailyStore', {
    extend: 'Ext.data.Store',
    model: 'Extensible.calendar.data.DailyModel',
	autoLoad: true,
	remoteFilter : true,
	autoSync: true,
	proxy: {
		type: 'ajax',
		api: {
				read: '/get_actual_daily_month/' + Ext.get("user-id").dom.innerHTML
		},
		reader: {
				type: 'json',
				root: 'daily',
				successProperty: 'success'
		}
	}
});
