Ext.define('Ext.calendar.data.Events', {

    statics: {
        getData: function() {
            var today = Ext.Date.clearTime(new Date()), 
                makeDate = function(d, h, m, s) {
                    d = d * 86400;
                    h = (h || 0) * 3600;
                    m = (m || 0) * 60;
                    s = (s || 0);
                    return Ext.Date.add(today, Ext.Date.SECOND, d + h + m + s);
                };
                
            return {
                "evts": [{
                    "id": 1001,
                    "cid": 2,
                    "title": "Vacation",
                    "task": 704,
                    "start": {datetime:153456464864646},
                    "end": {datetime:153456464864646},
                    "notes": "Have fun"
                }]
            }
        }
    }
});
