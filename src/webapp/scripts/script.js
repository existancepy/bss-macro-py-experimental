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

//get the value of input elements like checkboxes, dropdown and textboxes
function getInputValue(id){
    const ele = document.getElementById(id)
    //checkbox
    if (ele.tagName == "INPUT" && ele.type == "checkbox"){
        return ele.checked
    //textbox
    } else if (ele.tagName == "INPUT" && ele.type == "text"){
        const value = ele.value
        if (!value && (ele.dataset.inputType == "float" || ele.dataset.inputType == "int")) return 0
        if (!value) return ""
        return value
    //dropdown
    } else if (ele.tagName == "SELECT"){
        return ele.value.toLowerCase()
    }
}

async function loadSettings(){
    return await eel.loadSettings()()
}

async function loadAllSettings(){
    return await eel.loadAllSettings()()
}
//returns a object based on the settings
//proprties: an array of property names
//note: element corresponding to the property must have the same id as that property
function generateSettingObject(properties){
    let out = {}
    properties.forEach(x => {
        out[x] = getInputValue(x)
    })
    return out
}

//load fields based on the obj data
function loadInputs(obj){
    for (const [k,v] of Object.entries(obj)) {
        const ele = document.getElementById(k)
        if (ele.type == "checkbox"){
            ele.checked = v
        }else{
            ele.value = v
        }
    }
}

/*
=============================================
Header
=============================================
*/
//load the html
$("#header-placeholder").load("../htmlImports/persistent/header.html");

/*
=============================================
Utils
=============================================
*/

//utility to run after content has loaded
//to be fired as a callback in ajax .load
function textboxRestriction(ele, evt) {
    if (ele.dataset.inputLimit && ele.value.length >= ele.dataset.inputLimit) return false
    if (ele.dataset.inputType == "float"){
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode == 46) {
            //Check if the text already contains the . character
            if (ele.value.indexOf('.') === -1) {
                return true
            } else {
                return false
            }
        } else {
            if (charCode > 31 && (charCode < 48 || charCode > 57)) return false
        }
        return true;
    } else if (ele.dataset.inputType == "int"){
        return !(charCode > 31 && (charCode < 48 || charCode > 57))
    }
    }


//disable browser actions
/*
window.oncontextmenu = function(event) {
    // block right-click / context-menu
    event.preventDefault();
    event.stopPropagation();
    return false;
};
*/
window.addEventListener("keydown", (event) => {
    const key = event.key
    const disabledKeys = ["F1","F3","F5","F12"]
    if (disabledKeys.includes(key)){
        event.preventDefault()
        event.stopPropagation()
        return false
    } else if (event.ctrlKey && event.shiftKey && event.key == "I") {
        // block Strg+Shift+I (DevTools)
        event.preventDefault()
        event.stopPropagation()
        return false
    } else if (event.ctrlKey && event.shiftKey && event.key == "J") {
    // block Strg+Shift+J (Console)
    event.preventDefault()
    event.stopPropagation()
    return false
}
})
