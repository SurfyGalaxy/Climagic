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
    if (p == "actual-app") {
        visiblePage = "app"
        document.querySelector(".app").style.display = "flex";
        document.querySelector(".initial").style.display = "none";
        document.querySelector(".analysing").style.display = "none";
        document.documentElement.style.setProperty('--w', '1024px');
        document.documentElement.style.setProperty('--h', '735px');
    }
}

function isElementOutOfBounds(el) {
    const rect = el.getBoundingClientRect();

    // Check if any part of the element goes outside the viewport bounds
    const isPartiallyOffScreen =
        rect.top < 0 ||
        rect.left < 0 ||
        rect.bottom > (window.innerHeight || document.documentElement.clientHeight) ||
        rect.right > (window.innerWidth || document.documentElement.clientWidth);

    return isPartiallyOffScreen;
}


function renderGraph(data) {
    let dataset = [];
    data.forEach((d, i) => {
        dataset.push({ "para": i, "value": d })
    })
    document.querySelector("#wave-svg").innerHTML = ""
    document.querySelector("#wave-svg").setAttribute("viewBox","0 0 "+window.innerWidth + " 135")
    console.log(data)
    const width = window.innerWidth;
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
        .attr("id", "chartfill")
        .attr("fill", "url(#wave-gradient)");

    svg.append("path")
        .datum(dataset)
        .attr("d", lineGenerator)
        .attr("fill", "none")
        .attr("id", "chartline")
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
        .on("click", function (event, d) {
            showParaStats(d.para)
            if (document.querySelector(".active")) {
                document.querySelector(".active").classList.remove("active")
            }
            if (isElementOutOfBounds(document.querySelector("#para" + d.para))) {
                document.querySelector("#para" + d.para).scrollIntoView({ behavior: "smooth" })
            }
            document.querySelector("#para" + d.para).classList.add("active")
        });

}


function showParaStats(id) {
    paragraph = window.data[id]
    document.querySelector("#fks-para .value").innerText = paragraph.kinclaid_reading_ease
    document.querySelector("#fkg-para .value").innerText = paragraph.kinclaid_grade
    document.querySelector("#punc-dens-para .value").innerText = paragraph.punctuation_percent
    document.querySelector("#vocab-var-para .value").innerText = (paragraph.unique_words.length / paragraph.word_count) * 100
}
// QT Web Engine stuffs!
let backend = null;
function handlePyMsg(msg) {
    console.log(msg)
    msg = JSON.parse(msg)
    switch (msg.act) {
        case "picked":
            document.querySelector(".initial").classList.remove("not-picked")
            document.querySelector(".select").textContent = msg.name
            if (window.autoadvance) {
                sendToPython({ "act": "parsefile" })
                page("analysing")
            }
            break;
        case "data":
            page("actual-app")
            window.data = msg.data
            window.intensities = []
            document.querySelector(".story").innerHTML = ""

            msg.data.forEach((paragraph, i) => {
                if ("text" in paragraph) {
                    let paraEl = document.createElement("p")
                    paraEl.classList.add("para")
                    paraEl.innerText = paragraph.text
                    paraEl.id = "para" + i
                    paraEl.addEventListener("click", () => {
                        if (document.querySelector(".active")) {
                            document.querySelector(".active").classList.remove("active")
                        }
                        showParaStats(i)
                        paraEl.classList.add("active")
                    })
                    intensities.push((paragraph.exclamation * 2.0) + (paragraph.question * 1.5) + ((paragraph.repeated_words.reduce((sum, [word, count]) => sum + count, 0) / paragraph.word_count) * 1.0))

                    document.querySelector(".story").appendChild(paraEl)
                }
                else {
                    document.querySelector("#fks .value").innerText = paragraph.kinclaid_reading_ease
                    document.querySelector("#fkg .value").innerText = paragraph.kinclaid_grade
                    document.querySelector("#punc-dens .value").innerText = paragraph.punctuation_percent
                    document.querySelector("#vocab-var .value").innerText = (paragraph.unique_words.length / paragraph.word_count) * 100
                }
            })
            renderGraph(intensities)

        default:
            break;
    }
}
window.intensities = []
function initChannel() {
    try {
        if (typeof qt !== undefined && qt.webChannelTransport) {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                backend = channel.objects.backend;
                backend.python_message_signal.connect(handlePyMsg);
            })
        }
        else {
            alert("I don't know what you did but please make sure you're using the desktop app.")
            page("actual-app")
            renderGraph([0, 0.1, 0, 1, 0.5])

        }
    }
    catch {
        alert("I don't know what you did but please make sure you're using the desktop app.")
        page("actual-app")
        renderGraph([0, 0.1, 0, 1, 0.5])
    }

}
function sendToPython(msg) {
    if (backend) {
        backend.handle_js_message(JSON.stringify(msg))
    }
    else {
        alert("Not connected to the Python backend. Please use the desktop app.")
    }
}

window.autoadvance = false
document.querySelector(".select").addEventListener("click", () => {
    sendToPython({ "act": "pick_file" })
})
document.querySelector(".continue").addEventListener("click", () => {
    sendToPython({ "act": "parsefile" })
    page("analysing")
})
document.querySelector(".reload").addEventListener("click", () => {
    sendToPython({ "act": "parsefile" })
    page("analysing")
})

initChannel()
document.querySelector(".openfile").addEventListener("click", () => {
    window.autoadvance = true
    sendToPython({ "act": "pick_file" })
})
window.onresize = ()=>{
    renderGraph(intensities)
}