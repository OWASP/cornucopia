type DateStyle = Intl.DateTimeFormatOptions['dateStyle']

export class Text
{
    public static Capitalize(input : string)
    {
        const words = input.split(" ");

        for (let i = 0; i < words.length; i++) {
            words[i] = words[i].slice(0,1).toUpperCase() + words[i].slice(1,input.length);
        }

        return words.join(" ").replaceAll(' And ', ' and ').replaceAll(' Of ', ' of ');
    }

    public static Format(input : string)
    {
        input = String(input).replaceAll('-',' ')
        input = this.Capitalize(input);
        return input;
    }

    public static FormatPlain(input : string)
    {
        input = String(input).replaceAll('-',' ')
        return input;
    }

    public static FormatDate(input : string) : string
    {
        // This method expects 19 december 2020 as 20201219 (YYYMMDD)
        var dateString = '' + String(input);
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
        return String(input).trim().replaceAll('https','').replaceAll('http','').replaceAll('://','')
    }
}