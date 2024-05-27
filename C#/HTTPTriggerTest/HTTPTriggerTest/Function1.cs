using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Models;
using System.Data;
using System.Collections.Generic;
using System.Text;

namespace HTTPTriggerTest
{
    public static class Function1
    {
        [FunctionName("Function1")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");

            //string name = req.Query["name"];


            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();

            var result = JsonConvert.DeserializeObject<DataRows>(requestBody);

            var ResultList = new List<DataRows>();

            DataRows datarows = new DataRows
            {
                id = result.id,
                Club = result.Club,
                Type = result.Type,
                Environment = result.Environment, 
                ip = result.ip
               
             };

            ResultList.Add(datarows);

            var dtJson = JsonConvert.SerializeObject(ResultList);
            DataTable dt = (DataTable)JsonConvert.DeserializeObject(dtJson, (typeof(DataTable)));



            // name = name ?? data?.name;

            string responseMessage = dtJson;
              //  ? "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."
               // : $"Hello, {name}. This HTTP triggered function executed successfully.";

            return new OkObjectResult(responseMessage);
        }
    }
}
