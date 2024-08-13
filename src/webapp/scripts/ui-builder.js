//use javascript to add html elements
//avoids repetition of building the same elements

//commonly used
const slotArray = [1,2,3,4,5,6,7]

//id: id of input element
/*
    type property: the type of input element
    checkbox:
    type: {
        name: "checkbox",
        triggerFunction: "saveData()"
    }
    dropdown:
    type: {
        name: "dropdown",
        data: ["a","b","c"],
        triggerFunction: "saveData()",
        length: 13 //in rem units, defaults to 10 if not included
    }
    textbox:
    type: {
        name: "textbox",
        length: 13, //in rem units, defaults to 10 if not included
        triggerFunction: "saveData()",
        inputType: "float", //restrict the input values to only certain characters. Options are: string, float, int
        inputLimit: 5 //restrict the maximum number of characters allowed. If set to 0 or not included, no limit 
    }
*/


 
//create option elements in a already existing dropdown
//id: id of dropdown element
//data: array of values to set
function setDropdownData(id, data){
    //create the html
    html = ""
    data.forEach(x => {
        html += `<option value="${x}">${x}</option>`
    })
    //add it to the element
    document.getElementById(id).innerHTML = html
}

function buildInput(id, type){
    if (type.name == "checkbox"){
        return `<label class="checkbox-container" style="margin-top: 0.6rem;">
                    <input type="checkbox" id = ${id} onchange="${type.triggerFunction}">
                    <span class="checkmark"></span>
                </label>`
    }else if (type.name == "dropdown"){
        let html = `<select id="${id}" style="width: ${type.length? type.length: 10}rem; margin-top: 0.6rem;" onchange="${type.triggerFunction}" class="poppins-regular">`
        type.data.forEach(x => {
            let value = x
            if ($.type(value) === "string") value = value.replace(/[^\p{L}\p{N}\p{P}\p{Z}^$\n]/gu, '').trim().toLowerCase() //remove emojis and leading/trailing white space, also set to lowercase
            html += `<option value="${value}">${x}</option>`
        })
        html += "</select>"
        return html
    }
    else if (type.name == "textbox"){
        let html = `<input type="text" id="${id}" style="width: ${type.length? type.length: 10}rem; margin-top: 0.6rem;" class="poppins-regular textbox" data-input-type="${type.inputType}" data-input-limit="${type.inputLimit ? type.inputLimit : 0}" onkeypress="return textboxRestriction(this, event)" onchange="${type.triggerFunction}">`
        return html

    }

}

//parentElement: the parentElement to add the container to
//build a standard container for settings
//title: title of container
//settings: an array of objects
/*
[
    {
        id: "field-enable",
        title: "enable task",
        desc: "Enable gathering in field",
        type: input-type-object-here
    }
]
*/
function buildStandardContainer(parentElement,title,desc,settings){
    let out = `
        <div class = "poppins-medium standard-container" style="display: block; padding-top: 1rem;">
            <h2 id="${title.toLowerCase().replaceAll(" ","-")}">${title}</h2>
            <p style = "font-weight:500; font-size:1rem;">${desc}</p>
            <div class="seperator"></div>
    `
    //adjust padding right on the form based on the input type
    const inputPadding = {
        "checkbox": "10%",
        "dropdown": "5%",
        "textbox": "5%"
    }

    //add each setting
    settings.forEach((e,i) => {
        //note: if i > 0, set a margin-top
        //is it better to setup a parent div and use gap instead? yes
        out += `
        <form style="display: flex; align-items:flex-start; justify-content: space-between; padding-right: ${inputPadding[e.type.name]}; ${i? "margin-top:1rem": ""}";>
            <div style="width: 70%;">
                <label for="${e.id}">${e.title}</label>
                <p>${e.desc}</p>
            </div>
            ${buildInput(e.id,e.type)}
        </form>
        `
        out += "</form>"
    })

    out += "</div>"
    parentElement.innerHTML += (out)
}