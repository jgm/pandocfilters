Use this


```
blockdiag {
   A -> B -> C -> D;
   A -> E -> F -> G;
}
```

to get

```blockdiag
blockdiag {
   A -> B -> C -> D;
   A -> E -> F -> G;
}
```

with Äüö

```blockdiag
blockdiag {
   Ä -> Bü -> Cö -> D;
   Ä -> E -> F -> G;
}
```

See [(this is a link to whatever)](#whatever) for an example with options `{.plantuml #whatever caption="this is the caption" width=65%}`

```{.blockdiag #whatever caption="this is the caption" width=65%}
blockdiag {
   A -> B -> C -> D;
   A -> E -> F -> G;
}
```

DRY: no need to include the type twice

```{.blockdiag #whatever caption="this is the caption" width=65%}
   A -> B -> C -> D;
   A -> E -> F -> G;
```

# Samples

from <http://blockdiag.com/en/actdiag/examples.html>,
<http://blockdiag.com/en/nwdiag/nwdiag-examples.html>, ...


```{.blockdiag caption="blockdiag: shape of nodes" width=80%}

  // standard node shapes
  box [shape = box];
  square [shape = square];
  roundedbox [shape = roundedbox];
  dots [shape = dots];

  circle [shape = circle];
  ellipse [shape = ellipse];
  diamond [shape = diamond];
  minidiamond [shape = minidiamond];

  note [shape = note];
  mail [shape = mail];
  cloud [shape = cloud];
  actor [shape = actor];

  beginpoint [shape = beginpoint];
  endpoint [shape = endpoint];

  box -> square -> roundedbox -> dots;
  circle -> ellipse -> diamond -> minidiamond;
  note -> mail -> cloud -> actor;
  beginpoint -> endpoint;

  // node shapes for flowcharts
  condition [shape = flowchart.condition];
  database [shape = flowchart.database];
  terminator [shape = flowchart.terminator];
  input [shape = flowchart.input];

  loopin [shape = flowchart.loopin];
  loopout [shape = flowchart.loopout];

  condition -> database -> terminator -> input;
  loopin -> loopout;
```

```{.actdiag caption="actdiag: simple diagram" width=80%}
  write -> convert -> image

  lane user {
     label = "User"
     write [label = "Writing reST"];
     image [label = "Get diagram IMAGE"];
  }
  lane actdiag {
     convert [label = "Convert reST to Image"];
  }
```



```{.nwdiag caption="nwdiag: simple diagram" width=80%}
nwdiag {
  network dmz {
      address = "210.x.x.x/24"

      web01 [address = "210.x.x.1"];
      web02 [address = "210.x.x.2"];
  }
  network internal {
      address = "172.x.x.x/24";

      web01 [address = "172.x.x.1"];
      web02 [address = "172.x.x.2"];
      db01;
      db02;
  }
}
```


```{.nwdiag caption="nwdiag: peer networks" width=80%}
  inet [shape = cloud];
  inet -- router;

  network {
    router;
    web01;
    web02;
  }
```


```{.rackdiag caption="rackdiag: multiple racks" width=80%}
  // define 1st rack
  rack {
    16U;

    // define rack items
    1: UPS [2U];
    3: DB Server
    4: Web Server
    5: Web Server
    6: Web Server
    7: Load Balancer
    8: L3 Switch
  }

  // define 2nd rack
  rack {
    12U;

    // define rack items
    1: UPS [2U];
    3: DB Server
    4: Web Server
    5: Web Server
    6: Web Server
    7: Load Balancer
    8: L3 Switch
  }
```


```{.packetdiag caption="packetdiag: Structure of TCP Header"}
  colwidth = 32
  node_height = 72

  0-15: Source Port
  16-31: Destination Port
  32-63: Sequence Number
  64-95: Acknowledgment Number
  96-99: Data Offset
  100-105: Reserved
  106: URG [rotate = 270]
  107: ACK [rotate = 270]
  108: PSH [rotate = 270]
  109: RST [rotate = 270]
  110: SYN [rotate = 270]
  111: FIN [rotate = 270]
  112-127: Window
  128-143: Checksum
  144-159: Urgent Pointer
  160-191: (Options and Padding)
  192-223: data [colheight = 3]
```


```{.seqdiag caption="seqdiag: simple diagram" width=80%}
  browser  -> webserver [label = "GET /index.html"];
  browser <-- webserver;
  browser  -> webserver [label = "POST /blog/comment"];
              webserver  -> database [label = "INSERT comment"];
              webserver <-- database;
  browser <-- webserver;
```

```{.seqdiag caption="seqdiag: order of elements" width=80%}
seqdiag {
  # define order of elements
  # seqdiag sorts elements by order they appear
  browser; database; webserver;

  browser  -> webserver [label = "GET /index.html"];
  browser <-- webserver;
  browser  -> webserver [label = "POST /blog/comment"];
              webserver  -> database [label = "INSERT comment"];
              webserver <-- database;
  browser <-- webserver;
}
```

