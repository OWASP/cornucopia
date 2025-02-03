type DateStyle = Intl.DateTimeFormatOptions['dateStyle']

export class Text
{
    public static Capitalize(input : string)
    {
        return input.slice(0,1).toUpperCase() + input.slice(1,input.length).toLowerCase();
    }

    public static Format(input : string)
    {
        input = ('' + input).replaceAll('-',' ')
        input = this.Capitalize(input);
        return input;
    }

    public static FormatDate(input : string) : string
    {
        // This method expects 19 december 2020 as 20201219 (YYYMMDD)
        var dateString = '' + input;
        var year = parseInt(dateString.substring(0,4));
        var month = parseInt(dateString.substring(4,6));
        var day = parseInt(dateString.substring(6,8));
        var date = new Date(year, month-1, day);
        let result = date.getDate() + ' ' + date.toLocaleString('en-US', { month: 'short' }) + ', ' + date.getFullYear();
        return result
    }

    public static FormatDateAsDate(date : Date)
    {
        let result = date.getDate() 
        + ' '
         + date.toLocaleString('en-US', { month: 'short' }) 
         + ', ' 
         + date.getFullYear()
         + ' '
         + date.getUTCHours()
         + ':'
         + date.getUTCMinutes()
         + ':'
         + date.getUTCSeconds()
         + ' UTC'
        return result
    }

    public static DisplayLink(input : string) : string
    {
        return input.trim().replaceAll('https','').replaceAll('http','').replaceAll('://','')
    }
}