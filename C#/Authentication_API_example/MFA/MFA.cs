using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using System.Net;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Security.Cryptography;
using System.Text;
using System.Globalization;
using System.Net.Http;
using System.Collections.Generic;
using System.Xml.Linq;

namespace DuoMFAAuthHeader
{

    public class DuoAuth
    {


        [FunctionName("DuoAuthHeader")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)

        {
            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            dynamic data = JsonConvert.DeserializeObject(requestBody);

            //string TableName = data.Target_table;
            string URL = data.Relative_URL;
            string query = data.Query;

            DateTime date = (DateTime.UtcNow).AddHours(1);
            var method = "GET";
            var host = Environment.GetEnvironmentVariable("host"); ;
            var skey = Environment.GetEnvironmentVariable("secret_key");
            var ikey = Environment.GetEnvironmentVariable("integration_key");

            var stringHeader = Sign(method, host, URL,query, skey, ikey);


            var jsonresponse = new
            {
                Authorization = $"{stringHeader["Authorization"]}",
                date = $"{stringHeader["Date"]}"
            };


            return new OkObjectResult(jsonresponse);


        }

        static Dictionary<string, string> Sign(string method, string host, string path,string query, string skey, string ikey)
        {
            var now = DateTime.UtcNow.ToString("r");
            var canon = new List<string>
        {
            now,
            method.ToUpper(),
            host.ToLower(),
            path,
            query
        };

            var args = new List<string>();
           // canon.Add(string.Join("&", args));
            var stringToSign = string.Join("\n", canon);

            var sha1 = new HMACSHA1(Encoding.UTF8.GetBytes(skey));
            var sigBytes = sha1.ComputeHash(Encoding.UTF8.GetBytes(stringToSign));
            var auth = $"{ikey}:{BitConverter.ToString(sigBytes).Replace("-", "").ToLower()}";

            return new Dictionary<string, string>
        {
            { "Date", now },
            { "Authorization", $"Basic {Convert.ToBase64String(Encoding.UTF8.GetBytes(auth))}" }
        };
        }



    }


}