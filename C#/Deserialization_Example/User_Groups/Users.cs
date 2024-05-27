using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using JSONparserlocal.Models;
using System.Data;
using System.Net.Http;
using System.Data.SqlClient;

namespace Sophos_User_Groups
{
    public static class Sophos_Users
    {
        [FunctionName("HTTPTriggerexample")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");


            //Get the authorization, Tenant_ID, relative_URL, Query and page from the body

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            dynamic data = JsonConvert.DeserializeObject(requestBody);
            
            string Relative_URL = data.Relative_URL;
            string Authorization = data.Authorization;
            string Tenant_ID = data.Tenant_ID;
            string Query = data.Query;
            string URL = data.URL;


            //First call

            var url = $"{URL}{Relative_URL}?{Query}";
                    
            using var client = new HttpClient();
                   

            client.DefaultRequestHeaders.Add("Authorization", Authorization);
            client.DefaultRequestHeaders.Add("X-Tenant-ID", Tenant_ID);


            var response = client.GetAsync(url).Result;
            var content = response.Content.ReadAsStringAsync().Result;

            
            if (response.IsSuccessStatusCode)
            {
                Rootobject jsonobject = System.Text.Json.JsonSerializer.Deserialize<Rootobject>(content);


            //check number of pages

                int currentPage = jsonobject.pages.current;
                int totalPages = jsonobject.pages.total;


                DataTable newdataTable = TableConversor.CreateDataTable();
                           

                while (currentPage <= totalPages)

                {
                    var url_paginated = $"{url}&page={currentPage}";

                    var response_paginated = client.GetAsync(url_paginated).Result;
                    var content_paginated = response_paginated.Content.ReadAsStringAsync().Result;

                    Rootobject jsonresponse = System.Text.Json.JsonSerializer.Deserialize<Rootobject>(content_paginated);

                    DataTable dataTable = TableConversor.CopyToDataTable(jsonresponse, newdataTable);

                    currentPage++;

                }

                //Sink to Database

                string connectionString = Environment.GetEnvironmentVariable("SQL connection");

                TableConversor.BulkCopyToSqlServer(newdataTable, connectionString);

            }

            else

            {
                Console.WriteLine($"Error: {response.StatusCode}");
            }
                                   
            return new OkObjectResult(response.StatusCode);
        }
    }
}
