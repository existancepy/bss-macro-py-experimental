/*
=============================================
Gather Tab
=============================================
*/
var fieldNo = 1
//save the enabled status for the fields
async function saveEnabled(){
    const fields = (await loadSettings()).fields
    fields[fieldNo-1] = ele.value
    eel.saveProfileSetting("fields",fields)
}
function saveField(){
    const fieldProperties = ["shift_lock","field_drift_compensation", "pattern", "size","width","turn","turn_times","mins","backpack","return","whirligig_slot", "start_location", "distance"]
    const fieldData = generateSettingObject(fieldProperties)
    eel.saveField(document.getElementById("field").value,fieldData)
}

//load the field selected in the dropdown
async function loadAndSaveField(ele){
    const data = (await eel.loadFields()())[ele.value]
    loadInputs(data)
    //save
    const fields = (await loadSettings()).fields
    fields[fieldNo-1] = ele.value
    eel.saveProfileSetting("fields",fields)
}


async function switchGatherTab(target){
    fieldNo = target.id.split("-")[1]
    //remove the arrow indicator
    const selector = document.getElementById("gather-select")
    if (selector) selector.remove()
    Array.from(document.getElementsByClassName("gather-tab-item")).forEach(x => x.classList.remove("active")) //remove the active class
    target.classList.add("active")
    target.innerHTML = `<div class = "select-indicator" id = "gather-select"></div>` + target.innerHTML
    document.getElementById("gather-field").innerText = `Gather Field ${fieldNo}`
    const settings = await loadSettings()
    console.log(settings)
    //load the fields
    const fieldDropdown = document.getElementById("field")
    fieldDropdown.value = settings.fields[fieldNo-1]
    document.getElementById("field_enable").checked = settings.fields_enabled[fieldNo-1]
}

$("#gather-placeholder").load("../htmlImports/tabs/gather.html", () => switchGatherTab(document.getElementById("field-1"))) //load home tab, switch to field 1 once its done loading
.on("click", ".gather-tab-item", (event) => switchGatherTab(event.currentTarget)) //navigate between fields
