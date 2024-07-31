//load the html
$("#header-placeholder").load("../imports/header.html");

//change the styling of the purple buttons
//element: the purple button element
//label: the text labels of the button [not-active-label, active-label]
function purpleButtonToggle(element, labels){
    //check for active class
    if (element.classList.contains("active")){
        element.innerText = labels[0]
        element.classList.remove("active")
        return labels[1]
    }

    element.innerText = labels[1]
    element.classList.add("active")
    return labels[0]
    
}

//tab bar 
//switch tab
//start by hiding all tabs, then show the one that is relevant
//also remove all tabs' active class and add it back to the target one
function switchTab(event){
    const tabName = event.currentTarget.id.split("-")[0]
    //remove and hide
    Array.from(document.getElementsByClassName("content")).forEach(x => {
        x.style.display = "none"
    })
    Array.from(document.getElementsByClassName("sidebar-item")).forEach(x => {
        x.classList.remove("active")
    })
    //add and show
    event.currentTarget.classList.add("active")
    document.getElementById(`${tabName}-placeholder`).style.display = "flex"
}
//load and add event handlers
$("#tabs-placeholder")
.load("../imports/tabs.html")
.on("click",".sidebar-item", switchTab)
//home tab

//use a python function to open the link in the user's actual browser
function ahref(link){
    eel.openLink(link)
}

$("#home-placeholder")
.load("../imports/home.html") //load home tab
.on("click", "#log-btn",(event) => { //log button
    const result = purpleButtonToggle(event.currentTarget, ["Simple","Detailed"])
    document.getElementById("log-type").innerText = result
})
.on("click", "#start-btn",(event) => { //start button
    purpleButtonToggle(event.currentTarget, ["Start [F1]","Stop [F3]"])
})


