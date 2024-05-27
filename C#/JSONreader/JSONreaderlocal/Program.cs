using System.Text;
using System.Data;
using System.IO;
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Nodes;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using JSONparserlocal.Models;
using System.Data.SqlClient;
using System.Net.Http;
using System.Threading.Tasks;
using System.Net.Http.Headers;
//using Microsoft.Azure.Functions.Worker;
//using Microsoft.Extensions.Logging;


class JSONReader

{
    public static void Main()
    {

        // Get the Authorization, Tenant_ID, relative_URL and Query from the Body

        // var BodyContent = await new StreamReader(req.Body).ReadToEndAsync();

        //string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        //dynamic data = JsonConvert.DeserializeObject(requestBody);

        // RequestBody body = JsonConvert.DeserializeObject<RequestBody>(BodyContent);

        var url = "";


        using var client = new HttpClient();

        //var auth = new AuthenticationHeaderValue(authHeader);
        //client.DefaultRequestHeaders.Authorization = auth;

        //Get environmental variables

        string Tenant_ID = Environment.GetEnvironmentVariable("X-Tenant-ID");


        client.DefaultRequestHeaders.Add("Authorization", "Bearer ...");
        client.DefaultRequestHeaders.Add("X-Tenant-ID", Tenant_ID);


        var response = client.GetAsync(url).Result;
        var content = response.Content.ReadAsStringAsync().Result;

        if (response.IsSuccessStatusCode)
        {
            var result = JsonConvert.DeserializeObject(content);
           // Console.WriteLine(result);
        }
        else
        {
            Console.WriteLine($"Error: {response.StatusCode}");
        }


        Rootobject jsonobject = System.Text.Json.JsonSerializer.Deserialize<Rootobject>(content);

       // TableConversor converter = new TableConversor();

        DataTable dataTable = TableConversor.ConvertToDataTable(jsonobject);


        //Sink data to database


        string connectionString = "";


        TableConversor.BulkCopyToSqlServer(dataTable, connectionString);




    }




}



    






    
    

