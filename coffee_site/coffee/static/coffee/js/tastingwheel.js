function wheel(div, modifiers) {

   var lookup = {}
   mod_list = modifiers.split(",")
   mod_list.forEach(function(item) {
      var name = item.substring(1)
      console.log(name + "----" + typeof(lookup[name]))
      if (typeof(lookup[name]) === "undefined") {
         lookup[name] = 0.1
         console.log("--------" + typeof(lookup[name]))
      }
      if (item.substring(0,1) === "+") {
         lookup[name] = lookup[name] + 0.9
      }
      else if (item.substring(0,1) === "-") {
         //lookup[name] = lookup[name] - 0.1
      }
      //console.log(lookup[name])
   })
   console.log(mod_list)

   var width = 860,
       height = 800,
       radius = Math.min(width, height) / 3,
       color = d3.scale.category20c();

   var svg = d3.select(div).append("svg")
             .attr("width", width)
             .attr("height", height)
             //.on('load', modify(modifiers))
             .append("g")
                .attr("transform", "translate(" + width / 2 + "," + height * .50 + ")");

   var partition = d3.layout.partition()
        .sort(null)
        .size([2 * Math.PI, radius * radius])
        .value(function(d) {return 1;});

   var arc = d3.svg.arc()
        .startAngle(function(d) { return d.x * 1.0002; })
        .endAngle(function(d) { return d.x + d.dx; })
        // .innerRadius(function(d) { return Math.sqrt(d.y) / 1.5; })
        // .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });
        .innerRadius(function(d) {
           if (d.depth === 1) {
             return 62
          }
           else if (d.depth === 2) {
             return 170
          }
           else if (d.depth === 3) {
             return 290
            }
         return 0;
        })
        .outerRadius(function(d) {
           if (d.depth === 1) {
            return 170
           }
          else if (d.depth === 2) {
             return 290
          }
          else if (d.depth === 3) {
             return 390
         }
         return 0;
        });

   d3.json("/media/data.json", function(error, root) {
   if (error) throw error;

   var path = svg.datum(root).selectAll("path")
         .data(partition.nodes)
         .enter().append("g")

   path.append("path")
            .attr("id", function(d) { return d.name.replace("/", "-") })
            .attr("display", function(d) { return d.depth ? null : "none"; })
            //.attr("display", function(d) { return null; })
            .attr("d", arc)
            .attr("stroke", "black")
            .attr("stroke-opacity", 1)
            .style("fill", function(d) {
             if (d.color) return d3.rgb("#" + d.color)
             return color((d.children ? d : d.parent).name); })
            //.style("fill-rule", "evenodd")
            .style("opacity", 0.1)
            .style("opacity", function(d) {
               if (d.name.length > 0 && typeof(lookup[d.name]) !== "undefined") {
                  console.log(lookup[d.name])
                  console.log(d.name)
                  //d.parent.style("opacity", lookup[d.name])
                  //console.log(d.name + " " + d.parent.name)
                  if(d.parent.name !== "undefined" && d.parent.name.length > 0) {
                     //console.log("#" + d.parent.name)
                     //console.log(d.parent.name.length)
                     d3.select("#" + d.parent.name.replace("/", "-")).style("opacity", lookup[d.name])
                  }
                  return lookup[d.name]
               }
               return 0.1
            })
            //.style("stroke", "black")
            //.style("stroke-opacity", 1);

         path.append("text")
            .text(function(d) { return d.name})
            .classed("label", true)
            .attr("x", function(d) {
               return d.x; })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                  return "translate(" + arc.centroid(d) + ")" +
                          "rotate(" + rotationAngle(d) + ")";
            })
            .attr("dx", "6") // margin
            .attr("dy", ".35em") // vertical-align
            .attr("pointer-events", "none");

   });

   function rotationAngle(d) {
   // Offset the angle by 90 deg since the '0' degree axis for arc is Y axis, while
   // for text it is the X axis.
   var thetaDeg = (180 / Math.PI * (arc.startAngle()(d) + arc.endAngle()(d)) / 2 - 90);
   // If we are rotating the text by more than 90 deg, then "flip" it.
   // This is why "text-anchor", "middle" is important, otherwise, this "flip" would
   // a little harder.
   return (thetaDeg > 90) ? thetaDeg - 180 : thetaDeg;
   }

   d3.select(self.frameElement).style("height", height + 50 + "px");
   d3.select("path")
   //console.log("Done")
}

function modify(modifiers) {
   var lookup = {}
   mod_list = modifiers.split(",")
   mod_list.forEach(function(item) {
      //console.log(item.substring(1))
      lookup[item.substring(1)] = item.substring(0,1)
   })

}
