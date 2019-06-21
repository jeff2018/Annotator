var data = [
    {
        "name": "dbr:Ontology",
        "pages": ["Page 1", "Page 2", "Page 3", "Page 4", "Page 5", "Page 6"],
        "value": 6
    },
    {
        "name": "dbr:Visualization_(computer_graphics)",
        "pages": ["Page 1", "Page 2", "Page 5"],
        "value": 3
    }, {
        "name": "dbr:Concept",
        "pages": ["Page 1", "Page 2", "Page 3", "Page 4", "Page 5"],
        "value": 5
    }, {
        "name": "dbr:Information_visualization",
        "pages": ["Page 1", "Page 2", "Page 4", "Page 5"],
        "value": 4
    }, {
        "name": "dbr:Document",
        "pages": ["Page 1", "Page 2", "Page 4", "Page 5"],
        "value": 4
    }, {
        "name": "dbr:Teacher",
        "pages": ["Page 1"],
        "value": 1
    }, {
        "name": "dbr:Tool",
        "pages": ["Page 1", "Page 2", "Page 5"],
        "value": 3
    }, {
        "name": "dbr:File_manager",
        "pages": ["Page 1"],
        "value": 1
    }, {
        "name": "dbr:Computer_science",
        "pages": ["Page 1", "Page 2", "Page 4", "Page 5"],
        "value": 4
    }, {
        "name": "dbr:Ontology_(information_science)",
        "pages": ["Page 2", "Page 3", "Page 4", "Page 5"],
        "value": 4
    }, {
        "name": "dbr:Ontology_engineering",
        "pages": ["Page 2"],
        "value": 1
    }, {
        "name": "dbr:Information_retrieval",
        "pages": ["Page 2"],
        "value": 1
    }, {
        "name": "dbr:Parent",
        "pages": ["Page 3"],
        "value": 1
    }, {
        "name": "dbr:Child",
        "pages": ["Page 3"],
        "value": 1
    }, {
        "name": "dbr:Portable_Document_Format",
        "pages": ["Page 3"],
        "value": 1
    }, {
        "name": "dbr:Resource",
        "pages": ["Page 3", "Page 4", "Page 5"],
        "value": 3
    }, {
        "name": "dbr:Greek_language",
        "pages": ["Page 3"],
        "value": 1
    }, {
        "name": "dbr:Metaphysics",
        "pages": ["Page 3"],
        "value": 1
    }, {
        "name": "dbr:Philosopy",
        "pages": ["Page 3"],
        "value": 1

    }, {
        "name": "dbr:Paradox",
        "pages": ["Page 4"],
        "value": 1
    }, {
        "name": "dbr:Willard_Van_Orman_Quine",
        "pages": ["Page 4"],
        "value": 1
    }, {
        "name": "dbr:Circle",
        "pages": ["Page 4"],
        "value": 1
    }, {
        "name": "dbr:Computer_graphics",
        "pages": ["Page 1", "Page 5"],
        "value": 2
    }, {
        "name": "dbr:Carl_Linnaeus",
        "pages": ["Page 6"],
        "value": 1
    }, {
        "name": "dbr:Web_search_engine",
        "pages": ["Page 6"],
        "value": 1
    }, {
        "name": "dbr:A",
        "pages": ["Page 6"],
        "value": 1
    }, {
        "name": "dbr:Judge",
        "pages": ["Page 6"],
        "value": 1
    }, {
        "name": "dbr:Algorithm",
        "pages": ["Page 6"],
        "value": 1
    }, {
        "name": "dbr:Hebrew_language",
        "pages": ["Page 6"],
        "value": 1
    }, {
        "name": "dbr:Netherlands",
        "pages": ["Page 6"],
        "value": 1
    }, {
        "name": "dbr:Geometry",
        "pages": ["Page 6"],
        "value": 1
    },
    {
        "name": "dbr:Biology",
        "pages": ["Page 6"],
        "value": 1
    }

];

var pageArray = ["Page 1", "Page 2", "Page 3", "Page 4", "Page 5", "Page 6"];

var $this = $('.inner-div'); // targeted div
var offset = $this.offset();
var width = $this.width();
var height = $this.height();
var svg = d3.select("#svg_sunburst"),
    //width = document.body.clientWidth,
    //height = +svg.attr("height"),
    centerX = width * 0.5,
    centerY = height * 0.5,
    radius = width / 8
console.log("svg",svg)

//drawSunburst(data)
/*$(function(){
    $("#btn_sunburst").on('click',function(){
        console.log($(this).val())
        console.log("sunburst")
        drawSunburst(data)
       var bg = d3.select(".bubblegraph")
        if (bg) {
            bg.remove()
        }
    });
})*/



async function reverseData(dataArray){
    var newKeys = []
    var updatedJson=[]
    for(var i = 0; i < dataArray.length;i++){
        var pages =dataArray[i].pages
        var concept = dataArray[i].name
        //console.log(pages)
        //console.log("concept",concept)
        for(var k = 0; k < pages.length;k++){
            var p = pages[k]
            //console.log("page",p)
            if(!newKeys.includes(p)){
                newKeys.push(p)
                updatedJson.push({
                    "name": p,
                    "children":[],
                    //"value":0

                })
                //console.log(updatedJson[k].name)
            }
            for(var l = 0; l < updatedJson.length;l++){
                if(p === updatedJson[l].name){
                    //console.log("True",updatedJson[l].name,concept)
                    if(!updatedJson[l].children.includes(concept)){
                        updatedJson[l].children.push({"name":concept,
                        "value":pages.length})

                    }
                }
            }
        }
    }
    /*for(var m = 0; m <updatedJson.length;m++){
        updatedJson[m].value = updatedJson[m].children.length
    }*/
    var finalJson = []
    finalJson.push({
        "name": "Ontology Coverage Tool and Document Browser for Learning Material Exploration",
        "children": updatedJson
    })


    return finalJson
}
async function drawSunburst (data){
    svg = d3.select("#svg_sunburst")
    var updatedData = await reverseData(data)
    console.log("data",updatedData[0])
    var sunburstData = updatedData[0]
    var format = d3.format(",d");

    var arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
        .padRadius(radius * 1.5)
        .innerRadius(d => d.y0 * radius)
        .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

    function arcVisible(d) {
        return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
    }

    var partition = sunburstData=>{
        console.log("partition",sunburstData)

        var root = d3.hierarchy(sunburstData)
            .sum(function(d){

                return d.value
            })
            //.sort(null);

        console.log("hierarch",d3.hierarchy(sunburstData))
        console.log(d3.partition()
            .size([2 * Math.PI, root.height + 1])
            (root))
        return d3.partition()
            .size([2 * Math.PI, root.height + 1])
            (root);
    }

    var root = partition(sunburstData)
    root.each(d =>d.current =d)
    console.log("root",root)

    var color = d3.scaleOrdinal().range(d3.quantize(d3.interpolateRainbow, sunburstData.children.length + 1));

    console.log("desc",root.descendants())


    var g = svg.append("g")
        .attr("class","sunburst")
        .attr("transform", "translate(" + centerX + "," + centerY + ")")


    var path = g.append("g")
        .selectAll("path")
        .data(root.descendants().slice(1))
        .join("path")
        .attr("id",function(d,i){
            d.index = i
            return "path"+i
        })
        .attr("fill",function(d){
            while(d.depth > 1){
                d=d.parent;

            }
            return color(d.data.name)
        })
        .attr("value_fill",function(d){

            while(d.depth > 1){
                d=d.parent;

            }
            return color(d.data.name)
        })
        .attr("fill-opacity",function(d){
            return arcVisible(d.current) ? (d.children ? 0.6 :0.4):0;

        })
        .attr("value_fill-opacity",function(d){
            return arcVisible(d.current) ? (d.children ? 0.6 :0.4):0;

        })
        .attr("d",function(d){
            return arc(d.current)
        })

    path.filter(function(d) {
        //console.log("filter",d.children)
        //console.log(d.height)
        return d.children
        })
        .style("cursor","pointer")
        .on("click",clicked)

    path.filter(function(d){
        return d.height === 0
        })
        .style("cursor","pointer")
        .on("click", function(d){
            console.log(d)
            toggleColor(d)
        })


    path.append("title")
        .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);

    const label = g.append("g")
        .attr("class","label")
        .attr("pointer-events", "none")
        //.attr("text-anchor", "end")
        .style("user-select", "none")
        .selectAll("text")
        .data(root.descendants().slice(1))
        .join("text")
        .attr("dy", "0.35em")

        .attr("fill-opacity", d => +labelVisible(d.current))
        .attr("transform", d => labelTransform(d.current))
        .style("text-anchor","middle")
        .text(d => d.data.name)
        .attr("id", function (d, i) {
            return "t_" + i
        })

    /*
    .append("tspan")
    .attr("x", 0)
    .text(function(d) {
        return d.depth ? d.data.name.split("_")[0] : "";
    })
    .append("tspan")
    .attr("x", 0)
    .attr("dy", "1em")
    .text(function(d) {
        return d.depth ? d.data.name.split("_")[1] || "" : "";
    });*/
        /*        .style("font-size", "20px")



        .each(getSize)
        .style("font-size", function(d) {
            if(d.depth <= 1){
                return "30px"
            }
            else{
                console.log("current",d.current)
                console.log(d.depth)
                console.log("scale",d.data.name,d.scale+"px")
                var pieceSelect = "path"+parseInt(d.index )
                var bbox = document.getElementById(pieceSelect).getBBox()
                var height = bbox.height

                //return d.scale + "px";
                return 10+"px"
            }
        });/*
        .each(function (d, i) {
        var pieceSelect = "path"+parseInt(d.index )
        var bbox = document.getElementById(pieceSelect).getBBox()
        var height = bbox.height
        svg.select("#t_" + i)
            .call(wrap2, height)

        })

        .style("font-size", "15px")*/



    const parent = g.append("circle")
        .datum(root)
        .attr("r", radius)
        .attr("fill", "none")
        .attr("pointer-events", "all")
        .on("click", clicked);

    function clicked(p) {
        console.log("clicked",p)
        parent.datum(p.parent || root);

        root.each(d => d.target = {
            x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
            x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
            y0: Math.max(0, d.y0 - p.depth),
            y1: Math.max(0, d.y1 - p.depth)
        });

        const t = g.transition().duration(750);

        // Transition the data on all arcs, even the ones that aren’t visible,
        // so that if this transition is interrupted, entering arcs will start
        // the next transition from the desired position.
        path.transition(t)
            .tween("data", d => {
                const i = d3.interpolate(d.current, d.target);
                return t => d.current = i(t);
            })
            .filter(function (d) {
                return +this.getAttribute("fill-opacity") || arcVisible(d.target);
            })
            .attr("fill-opacity", d => arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0)
            .attrTween("d", d => () => arc(d.current));

        label.filter(function (d) {
            return +this.getAttribute("fill-opacity") || labelVisible(d.target);
        }).transition(t)
            .attr("fill-opacity", d => +labelVisible(d.target))
            .attrTween("transform", d => () => labelTransform(d.current));
    }

    function labelVisible(d) {
        //console.log("y1",d.y1, "y0",d.y0, d.x1,d.x0)
        return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
    }

    function labelTransform(d) {
        const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
        const y = (d.y0 + d.y1) / 2 * radius;
        return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
    }

    function toggleColor(d) {
       // console.log("togglecolor",d)
       // console.log(d3.select(d))
        var pieceSelect = "#path"+parseInt(d.index )
        var currentColor = d3.select(pieceSelect).attr("value_fill")

        currentColor = currentColor === "lightgrey" ? color(d.parent.data.name) : "lightgrey";

        d3.select(pieceSelect).attr("value_fill", currentColor);
        d3.select(pieceSelect).style("fill", currentColor);

    }
    function getSize(d) {
        console.log("getSize",d)
        console.log(this)
        var textLength = this.getComputedTextLength()
        var pieceSelect = "path"+parseInt(d.index )
        console.log(document.getElementById(pieceSelect))


        var bbox = document.getElementById(pieceSelect).getBBox(),


            scale = Math.max(bbox.width/textLength, bbox.height/textLength);
        console.log(d.data.name,bbox.width/textLength,bbox.height/textLength)
        console.log("bbox",bbox)
        console.log("getComputedTextLength",this.getComputedTextLength())


        d.scale = scale -1;


    }


}
function wrap2(text, width) {
    //console.log("wrap",text,width)
    text.each(function () {
        var text = d3.select(this)
        var joinOperator = " "
        if (text.text().includes("-")) {
            joinOperator = "-"
        }
        if (text.text().includes("_")) {
            joinOperator = "_"
        }
        var words = text.text().split(/[ _-]+/).reverse(), ///[ _]+/ /\s+/
            word,
            counter = 0,
            line = [],
            lineNumber = 0,
            lineHeight = 1.2, // ems
            startBox = (lineHeight / 2) / 2,
            x = text.attr("x"),
            y = text.attr("y"),
            dy = text.attr("dy") ? text.attr("dy") : 0,
            totalLines = words.length,
            start = -(lineHeight / 2) * (totalLines - 1),
            resultingLines = [],
            adjustment = 0;

        if (totalLines > 1) {
            if (!isEven(totalLines)) {
                start = startBox - (lineHeight / 2) * (totalLines - 1);
            } else {
                start = startBox - (lineHeight / 2) - (2 / totalLines);
            }

        } else {
            start = startBox
        }

        tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", start + "em").attr("id", "start").attr("value", start);

        //console.log(tspan)
        //console.log(words)
        //console.log(totalLines,lineHeight,lineHeight*totalLines)


        while (word = words.pop()) {
            //console.log(word)

            line.push(word);
            //console.log(line)
            tspan.text(line.join(joinOperator));
            //console.log(line.join(joinOperator))
            //console.log(tspan.node())
            //console.log(tspan.node().getComputedTextLength() > width)
            //console.log(tspan.node().getComputedTextLength(), width)

            if (tspan.node().getComputedTextLength() > width) {
                //console.log("if",tspan.node().getComputedTextLength(), width)

                var last = line.pop();
                //console.log(last)
                resultingLines.push(last)
                tspan.text(line.join(joinOperator));
                line = [word];
                //console.log(line,lineNumber,lineHeight,dy,resultingLines.length)
                var modifier;


                if (totalLines > 1) {
                    if (words.length !== 0) {
                        modifier = ++lineNumber * lineHeight + (start * (totalLines - 1))

                    } else {
                        modifier = ++lineNumber * lineHeight + (start * (resultingLines.length - 1))
                        //console.log(resultingLines.length < totalLines)
                        if (resultingLines.length < totalLines) {
                            var old = text.selectAll("tspan").attr("value")
                            //console.log(old)
                            adjustment = lineHeight / 2
                            text.selectAll("tspan").attr("dy", parseFloat(old) + adjustment + "em").attr("value", parseFloat(old) + adjustment)
                        }

                    }
                } else {
                    modifier = 0
                }
                counter = counter + 1

                tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", modifier + parseFloat(adjustment) + "em").attr("id", "if").attr("value", modifier).text(word);
                //console.log(lineNumber)
            } else {
                resultingLines.shift()
                resultingLines.push(line.join(" "))
                if (words.length === 0 && totalLines > 1) {
                    var old = text.selectAll("tspan").attr("value")
                    //console.log(old)
                    adjustment = lineHeight / 2
                    text.selectAll("tspan").attr("dy", parseFloat(old) + adjustment + "em").attr("value", parseFloat(old) + adjustment)
                }
            }

        }


    });


}