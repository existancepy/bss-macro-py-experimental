/*
=============================================
Config Tab
=============================================
*/
async function loadCollect(){
    const settings = await loadAllSettings()
    loadInputs(settings)
}

$("#collect-placeholder", loadCollect)
.load("../htmlImports/tabs/collect.html") //load config tab
