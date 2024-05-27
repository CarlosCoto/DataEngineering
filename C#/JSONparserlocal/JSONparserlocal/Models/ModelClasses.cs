using System;
using System.Collections.Generic;


namespace Models
{

    public class Column
    {
        public string? name { get; set; }
        public string? type { get; set; }
    }
    public class Table
    {
        public string? name { get; set; }
        public List<Column>? columns { get; set; }
        public List<List<string>>? rows { get; set; }
    }
    public class RootObject
    {
        public List<Table>? tables { get; set; }
    }

    //public class RootData
    //{
    //    public List<Data>? data { get; set; }

    //}

    //public class Data
    //{
    //    public string? data_1 { get; set; }
    //    public string? data_2 { get; set; }
    //    public string? data_3 { get; set; }
    //    public string? data_4 { get; set; }
    //    public string? data_5 { get; set; }
    //    public string? data_6 { get; set; }
    //    public string? data_7 { get; set; }
    //    public string? data_8 { get; set; }
    //    public string? data_9 { get; set; }

    //}


    //public class RowData
    //{
    //    public string? Row1 { get; set; }
    //    public string? Row2 { get; set; }
    //    public string? Row3 { get; set; }
    //    public string? Row4 { get; set; }
    //    public string? Row5 { get; set; }
    //    public string? Row6 { get; set; }
    //    public string? Row7 { get; set; }
    //    public string? Row8 { get; set; }
    //    public string? Row9 { get; set; }
    //    public string? Row10 { get; set; }


    //}

}






