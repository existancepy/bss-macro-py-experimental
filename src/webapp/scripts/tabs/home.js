/*
=============================================
Home Tab
=============================================
*/

//use a python function to open the link in the user's actual browser
function ahref(link){
    eel.openLink(link)
}

//toggle the start/stop button visuals
eel.expose(toggleStartStop)
function toggleStartStop(){
    return purpleButtonToggle(document.getElementById("start-btn"), ["Start [F1]","Stop [F3]"])
}

eel.expose(log)
function log(time = "", msg = "", color = ""){
    document.getElementById("log")
    let timeText = ""
    if (time) timeText = `[${time}]`
    const html = `
    <div class = "log-msg"><span style="background-color: #${color}; align-self: start"></span>${timeText} ${msg}</div>
    `
    const logs = document.getElementById("logs")
    logs.innerHTML += html
    logs.scrollTop = logs.scrollHeight;
}

//returns a html string for the task
function taskHTML(title, desc=""){
    const html = `
    <div style="margin-top: 1rem;">
        <div style="font-size: 1.1rem;">${title}</div>
        <div style="font-size: 0.9rem; color: #ADB5BD;">${toTitleCase(desc)}</div>
        <div style="background-color: #949393; height: 1px; width: 95%; margin-top: 0.4rem;"></div>
    </div>
    `
    return html
}
/*

*/
//load the tasks
//also set max-height for logs
async function loadTasks(){
    const setdat = await loadAllSettings()
    let out = ""
    //load collect
    for (const [k, v] of Object.entries(collectEmojis)) {
        if (!setdat[k]) continue
        out += taskHTML("Collect", `${v} ${toTitleCase(k.replaceAll("_", " "))}`)
    }
    //planters
    if (setdat["planters_mode"]){
        const type = setdat["planters_mode"] == 1 ? "Manual" : "Auto"
        out += taskHTML("Planters", type)
    }
    //load kill
    for (let [k, v] of Object.entries(killEmojis)) {
        if (!setdat[k]) continue
        if (k == "rhinobeetle") k = "rhino beetle"
        out += taskHTML("Kill", `${v} ${toTitleCase(k.replaceAll("_", " "))}`)
    }
    //load the gather
    for(let i = setdat.fields_enabled.length-1; i >= 0; i--){
        if (!setdat.fields_enabled[i]) continue
        const field = setdat.fields[i]
        out += taskHTML(`Gather ${i+1}`,`${fieldEmojis[field.replaceAll(" ","_")]} ${field}`)
    }
    //display the tasks
    document.getElementById("task-list").innerHTML = out
}



$("#home-placeholder")
.load("../htmlImports/tabs/home.html", loadTasks) //load home tab
.on("click", "#log-btn",(event) => { //log button
    const result = purpleButtonToggle(event.currentTarget, ["Simple","Detailed"])
    document.getElementById("log-type").innerText = result
})
.on("click", "#start-btn",(event) => { //start button
    //no need to change display, python will trigger toggleStartStop
    if (event.currentTarget.classList.contains("active")){
        eel.stop()
    }else{
        eel.start()
    }
})