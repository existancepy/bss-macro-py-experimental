/*
=============================================
Planters Tab
=============================================
*/

//when the planter slider changes
function changePlanterMode(){
    const ele = document.getElementById("planters_mode")
    saveSetting(ele, 'profile')
    //show the corresponding tab
    const planterMode = {
        1: "manual",
        2: "auto"
    }
    Array.from(document.getElementsByClassName("planter-tab")).forEach(x => x.style.display="none")
    //ele.value doesnt
    if (ele.value > 0) document.getElementById(`planters-${planterMode[ele.value]}`).style.display = "block"
    
}

function loadPlanters(){
    const cycleElement = document.getElementById("manual-planters-cycles")
    for (i=1; i < 6;i++){
        const html = 
        `
        <div class="seperator" style="margin-bottom: 1rem;"></div>
        <h3 class="poppins-semibold">Cycle ${i}</h3>
        <table style="margin-top: 1rem; row-gap: 1rem;">
            <tr>
                <td><h4 class="poppins-regular">Planters:</h4></td>
                <td><select id="cycle${i}_1_planter" onchange="saveSetting(this, 'profile')" class="poppins-regular manual-planters-planters"></select></td>
                <td><select id="cycle${i}_2_planter" onchange="saveSetting(this, 'profile')" class="poppins-regular manual-planters-planters"></select></td>
                <td><select id="cycle${i}_3_planter" onchange="saveSetting(this, 'profile')" class="poppins-regular manual-planters-planters"></select></td>
            </tr>
            <tr>
                <td><h4 class="poppins-regular">Fields:</h4></td>
                <td><select id="cycle${i}_1_field" onchange="saveSetting(this, 'profile')" class="poppins-regular manual-planters-field"></select></td>
                <td><select id="cycle${i}_2_field" onchange="saveSetting(this, 'profile')" class="poppins-regular manual-planters-field"></select></td>
                <td><select id="cycle${i}_3_field" onchange="saveSetting(this, 'profile')" class="poppins-regular manual-planters-field"></select></td>
            </tr>
            <tr>
                <td><h4 class="poppins-regular">Gather in Planter Field:</h4></td>
                <td><label class="checkbox-container" style="margin-top:-0.6rem">
                    <input type="checkbox" id = "cycle${i}_1_gather" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
                <td><label class="checkbox-container" style="margin-top:-0.6rem">
                    <input type="checkbox" id = "cycle${i}_2_gather" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
                <td><label class="checkbox-container" style="margin-top:-0.6rem">
                    <input type="checkbox" id = "cycle${i}_3_gather" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
            </tr>
        </table>
        `
        cycleElement.innerHTML += html
    }
    //no need to call the load function, another tab will call it 
    //show the planter tab
    changePlanterMode()
}

$("#planters-placeholder")
.load("../htmlImports/tabs/planters.html", loadPlanters) 
