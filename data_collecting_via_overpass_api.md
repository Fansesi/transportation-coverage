# Data Collecting via Overpass API

[Overpass API](https://overpass-turbo.eu/) has query language that is easy to get used to. One may use the *wizard* tab to get started quickly. Furthermore, here are some examples that I've found to be fruitful for İstanbul:

```
[out:csv (::id, ::lat,::lon, name)];

//nwr["operator"="Metro İstanbul"]({{bbox}});
//nwr["network"="İstanbul Metrosu"]({{bbox}});
//nwr["operator"="TCDD "]({{bbox}});

// print results
out geom;
```

```
[out:csv (::id, ::lat,::lon, name)];

// gather results
//nwr["operator"="İETT"]({{bbox}});
//nwr["network"="İETT"]({{bbox}});
nwr["highway"="bus_stop"]({{bbox}});

// print results
out geom;
```

**NOTE:** To filter using two keywords at the same time:

```
nwr["highway"="bus_stop"]["network"="İETT"]({{bbox}});
```
