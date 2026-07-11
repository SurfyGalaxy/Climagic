let chars = "abcdefghijklmnopqrstuvwxyz              ,.!?";
function doRandom() {
    if (visiblePage == "analysing") {
        if (Math.round(Math.random())) {
            let c = chars[Math.floor(Math.random() * chars.length)]
            console.log("added char", c)
            document.querySelector(".textanim").textContent += c
            setTimeout(doRandom, 10)

        }
        else {
            setTimeout(doRandom, 70)

        }
    }
    document.querySelector(".textanim").scrollTo(0, document.querySelector(".textanim").scrollHeight)
}

let visiblePage = "initial"

function page(p) {
    if (p == "analysing") {
        visiblePage = "analysing"
        document.querySelector(".analysing").style.display = "flex";
        document.querySelector(".initial").style.display = "none";
        document.documentElement.style.setProperty('--w', '500px');
        document.documentElement.style.setProperty('--h', '500px');
        setTimeout(doRandom, 10)
    }
    if (p == "initial") {
        visiblePage = "initial"
        document.querySelector(".initial").style.display = "flex";
        document.querySelector(".analysing").style.display = "none";
        document.documentElement.style.setProperty('--w', '500px');
        document.documentElement.style.setProperty('--h', '500px');
    }
    if(p == "actual-app"){
        visiblePage = "app"
        document.querySelector(".app").style.display = "flex";
        document.querySelector(".initial").style.display = "none";
        document.querySelector(".analysing").style.display = "none";
        document.documentElement.style.setProperty('--w', '1024px');
        document.documentElement.style.setProperty('--h', '735px');
    }
}


page("actual-app")


function renderGraph(data){
        let dataset = [];
        data.forEach((d,i)=>{
            dataset.push({"para":i, "value": d})
        })
        console.log(data)
        const width = 1024;
        const height = 135;
        const svg = d3.select("#wave-svg");

        // 2. Setup Scales (maps data values to SVG pixel coordinates)
        const xScale = d3.scaleLinear()
            .domain([0, dataset.length - 1])
            .range([0, width]);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(dataset, d => d.value)])
            .range([height, 20]); // 20px padding at top so wave doesn't clip

        // 3. Define the Wave Shapes (Smooth Splines)
        const lineGenerator = d3.line()
            .x((d, i) => xScale(i))
            .y(d => yScale(d.value))
            .curve(d3.curveBasis); // Makes it a smooth "wave"

        const areaGenerator = d3.area()
            .x((d, i) => xScale(i))
            .y0(height) // Bottom base of the wave
            .y1(d => yScale(d.value))
            .curve(d3.curveBasis);

        // 4. Create the Gradient Fill
        const defs = svg.append("defs");
        const gradient = defs.append("linearGradient")
            .attr("id", "wave-gradient")
            .attr("x1", "0%").attr("y1", "0%")
            .attr("x2", "0%").attr("y2", "100%");
        
        gradient.append("stop").attr("offset", "0%").attr("stop-color", "#9FF4E5").attr("stop-opacity", 0.3);
        gradient.append("stop").attr("offset", "100%").attr("stop-color", "#9FF4E5").attr("stop-opacity", 0.0);
        svg.append("path")
            .datum(dataset)
            .attr("d", areaGenerator)
            .attr("id","chartfill")
            .attr("fill", "url(#wave-gradient)");

        svg.append("path")
            .datum(dataset)
            .attr("d", lineGenerator)
            .attr("fill", "none")
            .attr("id","chartline")
            .attr("stroke", "#38bdf8")
            .attr("stroke-width", 4);
    

        // 6. Create Invisible "Hit Boxes" for wide, forgiving click areas
        const barWidth = width / dataset.length;
        
        const interactionGroups = svg.selectAll(".interaction-group")
            .data(dataset)
            .enter()
            .append("g")
            .attr("class", "interaction-group");

        // The clickable rectangle area
        interactionGroups.append("rect")
            .attr("class", "click-target")
            .attr("x", (d, i) => xScale(i) - (barWidth / 2))
            .attr("y", 0)
            .attr("width", barWidth)
            .attr("height", height)
            .on("click", function(event, d) {
                // --- YOUR CUSTOM CODE HERE ---
                console.log(d)
                // -----------------------------
            });

}
renderGraph([0,0.1,0,1,0.5])