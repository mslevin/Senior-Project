   var tastesString = ""




   var width = 800,
       height = 800,
       radius = Math.min(width, height) / 3,
       color = d3.scale.category20c();

   var svg = d3.select(".tastingwheel").append("svg")
             .attr("width", width)
             .attr("height", height)
             .on('load', function() {console.log("yas")})
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

   d3.json("../../media/data.json", function(error, root) {
   if (error) throw error;

   var path = svg.datum(root).selectAll("path")
         .data(partition.nodes)
         .enter().append("g")

   path.append("path")
            .attr("id", function(d) { return d.name })
            .attr("display", function(d) { return d.depth ? null : "none"; })
            //.attr("display", function(d) { return null; })
            .attr("d", arc)
            .attr("class", "inactive")
            .attr("stroke", "#fff")
            .style("fill", function(d) {
             if (d.color) return d3.rgb("#" + d.color)
             return color((d.children ? d : d.parent).name); })
            .style("fill-rule", "evenodd")
            .style("stroke", "black")
            .on("mouseenter", function(d) {
               d3.select(this).classed({'active':true, 'inactive':false})
            })
            .on("mouseleave", function(d) {
               d3.select(this).classed({'active':false, 'inactive':true})
            })
            .on("click", function(d) {
               var elem = d3.select(this)
               elem.classed({'stayactive': !elem.classed('stayactive')})

               console.log(d.parent)
               d3.selectAll("path").filter(function(f) { f.name === d.parent.name} ).classed({'stayactive': !elem.classed('stayactive')})

               tastesString = tastesString + d.name
               // other stuff needs to happen here to save the info!
               /// SAVE the stuff when the thing is submitted
               // because it'll be hard to account for deselecting things
               // when the page is submitted just select everything with .stayactive
            })

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
