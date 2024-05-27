
using System.Data;

public class Rootobject
{
    public Item[] items { get; set; }

    public Pages pages { get; set; }


}

public class Pages
{
    public int current { get; set; }
    public int size { get; set; }
    public int total { get; set; }
    public int items { get; set; }
    public int maxSize { get; set; }
}

public class Item
{
    public string id { get; set; }
    public string name { get; set; }
    public string displayName { get; set; }
    public string description { get; set; }

    public string domain { get; set; }
    public Groups groups { get; set; }
    public Source source { get; set; }
    public Users users { get; set; }
    public Tenant tenant { get; set; }
    public string ?createdAt { get; set; }
    public string ?updatedAt { get; set; }
}

public class Groups
{
    public int total { get; set; }
    public int itemsCount { get; set; }
    public Item1[] items { get; set; }
}

public class Item1
{
    public string id { get; set; }
    public string name { get; set; }
    public string displayName { get; set; }
}

public class Source
{
    public string type { get; set; }
}

public class Users
{
    public int total { get; set; }
    public int itemsCount { get; set; }
    public Item2[] items { get; set; }
}

public class Item2
{
public string id { get; set; }
public string name { get; set; }
}

public class Tenant
{
    public string id { get; set; }
}



//public class DataRow
//{
//    public string ?user_id { get; set; }
//    public string ?user_name { get; set; }


//}
