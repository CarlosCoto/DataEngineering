using System.Text;
using System.Data;
using System.IO;
using System.Reflection;
using Newtonsoft.Json;
using Models;

class JSONReader

{
    public static void Main()
    {
        //  var ResultList = new List<RowData>();

        StreamReader jsonTemp = new StreamReader("C:\\Users\\carlos.sarmiento\");

        string currentLine = jsonTemp.ReadLine();

        var result = JsonConvert.DeserializeObject<RootObject>(currentLine);
            
        var rowData = result.tables.SelectMany(x => x.rows.Select(c => c));

        DataTable dt = new DataTable();

        for (int i = 0; i < result.tables[0].columns.Count; i++)

        {
                dt.Columns.Add(result.tables[0].columns[i].name, typeof(string));
        }

        foreach (var row in rowData)
        {

            DataRow dataRow = dt.NewRow();
            dt.Rows.Add(row.ToArray());
          

        }



    }

   

}