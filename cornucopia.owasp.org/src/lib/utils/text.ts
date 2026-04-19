type DateStyle = Intl.DateTimeFormatOptions['dateStyle']

export class Text
{
    public static Capitalize(input : string)
    {
        // FIX: Added safety guard to prevent 'slice' error on undefined/null
        if (!input) return "";

        const words = input.split(" ");

        for (let i = 0; i < words.length; i++) {
            // Added check for empty strings within words
            if (words[i].length > 0) {
                words[i] = words[i].slice(0,1).toUpperCase() + words[i].slice(1, input.length);
            }
        }

        return words.join(" ").replaceAll(' And ', ' and ').replaceAll(' Of ', ' of ');
    }

    public static Format(input : string)
    {
        if (!input) return ""; 
        input = String(input).replaceAll('-',' ')
        input = this.Capitalize(input);
        return input;
    }

    public static FormatPlain(input : string)
    {
        if (!input) return "";
        input = String(input).replaceAll('-',' ')
        return input;
    }

    public static convertToTitleCase( str: string ) : string {
        if (!str) return "";
        return str.toLowerCase().replace(/\b\w/g, function(char) {
            return char.toUpperCase();
        });
    }

    public static FormatDate(input : string) : string
    {
        if (!input) return "";
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
        if (!date) return "";
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
        if (!input) return "";
        return String(input).trim().replaceAll('https','').replaceAll('http','').replaceAll('://','')
    }
}