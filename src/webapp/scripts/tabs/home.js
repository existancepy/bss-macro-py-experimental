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


$("#home-placeholder")
.load("../htmlImports/tabs/home.html") //load home tab
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