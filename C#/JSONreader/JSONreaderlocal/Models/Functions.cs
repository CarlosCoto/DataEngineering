using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace JSONparserlocal.Models
{
    public class TableConversor

    {

        public static DataTable ConvertToDataTable(Rootobject jsonobject)

        {


            DataTable dataTable = new DataTable();
            dataTable.Columns.Add("Group_ID", typeof(string));
            dataTable.Columns.Add("Group_Name", typeof(string));
            dataTable.Columns.Add("DisplayName", typeof(string));
            dataTable.Columns.Add("Description", typeof(string));
            dataTable.Columns.Add("Domain", typeof(string));
            dataTable.Columns.Add("source_type", typeof(string));
            dataTable.Columns.Add("TotalUsers", typeof(int));
            dataTable.Columns.Add("user_id", typeof(string));
            dataTable.Columns.Add("user_name", typeof(string));
            dataTable.Columns.Add("tenant_id", typeof(string));
            dataTable.Columns.Add("createdAt", typeof(string));
            dataTable.Columns.Add("updatedAt", typeof(string));

            // Populate rows of the DataTable using the deserialized JSON object


            foreach (var item in jsonobject.items)

            {

                var itemUsers = Equals(item.users.itemsCount, 0) ? Enumerable.Repeat(new Item2 { id = "", name = "" }, 1) : item.users.items;

                foreach (var user in itemUsers)
                {
                    DataRow dataRow = dataTable.NewRow();
                    dataRow["Group_ID"] = item.id;
                    dataRow["Group_Name"] = item.name;
                    dataRow["DisplayName"] = item.displayName;
                    dataRow["Description"] = item.description;
                    dataRow["Domain"] = item.domain;
                    dataRow["source_type"] = item.source.type;
                    dataRow["TotalUsers"] = item.users.total;
                    dataRow["user_id"] = user.id;
                    dataRow["user_name"] = user.name;
                    dataRow["tenant_id"] = item.tenant.id;
                    dataRow["createdAt"] = item.createdAt;
                    dataRow["updatedAt"] = item.updatedAt;

                    dataTable.Rows.Add(dataRow);
                }

            }


            return dataTable;

        } //end of first function


    public static void  BulkCopyToSqlServer (DataTable dataTable, string connectionString)

        {

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                //create table dbo.bandwidth_stg -- sp_handlestagingdata --> Delete old data, move new data
                connection.Open();
                using (SqlBulkCopy bulkCopy = new SqlBulkCopy(connection))
                {
                    foreach (DataColumn c in dataTable.Columns)
                    {
                        var columnName = c.ColumnName;
                        try
                        {
                            bulkCopy.ColumnMappings.Add(columnName, columnName);
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine($"Error in {columnName} mapping: {ex.Message}");
                        }
                    }
                    bulkCopy.DestinationTableName = "[schema].[table_name]";
                    try
                    {
                        bulkCopy.WriteToServer(dataTable);
                    }
                    catch (Exception ex)
                    {

                        Console.WriteLine(ex.Message);
                    }
                }
            }

        }


    }
}
