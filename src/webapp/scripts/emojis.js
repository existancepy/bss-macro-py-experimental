/*
=============================================
Emoji list
=============================================
*/


//utility function to convert them to an array
function toEmojiArray(emojiObj){
    out = []
    for (const [k,v] of Object.entries(emojiObj)) {
        out.push(`${v} ${toTitleCase(k.replaceAll("_"," "))}`)
    }
    return out
}

//same as toEmojiArray, but for images
//if v is null, no img is made
//if right is true, image appears on the right of text
function toImgArray(emojiObj, right = false){
    out = []
    for (const [k,v] of Object.entries(emojiObj)) {
        const imgHTML = v? `<img src="./assets/icons/${v}.png">`: ''
        const text = toTitleCase(k.replaceAll("_"," "))
        out.push( right? `${text}${imgHTML}`: `${imgHTML}${text}`)
    }
    return out
}

//https://emojidb.org/
const fieldEmojis = {
    sunflower: "🌻",
    dandelion: "🌼",
    mushroom: "🍄",
    blue_flower: "🔷",
    clover: "🍀",
    strawberry: "🍓",
    spider: "🕸️",
    bamboo: "🐼",
    pineapple: "🍍",
    stump: "🐌",
    cactus: "🌵",
    pumpkin: "🎃",
    pine_tree: "🌲",
    rose: "🌹",
    mountain_top: "⛰️",
    pepper: "🌶️",
    coconut: "🥥"
}

const collectEmojis = {
    wealth_clock: "🕒",
    blueberry_dispenser: "🔵",
    strawberry_dispenser: "🍓",
    royal_jelly_dispenser: "💎",
    treat_dispenser: "🦴",
    ant_pass_dispenser: "🎫",
    glue_dispenser: "🧴",
    stockings: "🧦",
    feast: "🍽️",
    samovar: "🏺",
    snow_machine: "❄️",
    lid_art: "🖼️",
    candles: "🕯️",
    wreath: "🎄",
    sticker_printer: "🖨️",
    mondo_buff: "🐣",
}

const killEmojis = {
    stinger_hunt: "😈",
    scorpion: "",
    werewolf: "",
    ladybug: "",
    rhinobeetle: "",
    spider: "",
    mantis: "",
    ant_challenge: "🎯",
    coconut_crab: "",
    stump_snail: "🐌",
}

const fieldNectarIcons = {
    none: null,
    sunflower: "satisfying",
    dandelion: "comforting",
    mushroom: "motivating",
    blue_flower: "refreshing",
    clover: "invigorating",
    strawberry: "refreshing",
    spider: "motivating",
    bamboo: "comforting",
    pineapple: "satisfying",
    stump: "motivating",
    cactus: "invigorating",
    pumpkin: "satisfying",
    pine_tree: "comforting",
    rose: "motivating",
    mountain_top: "invigorating",
    pepper: "invigorating",
    coconut: "refreshing"
}

const planterIcons = {
    none: null,
    paper: "paper_planter",
    ticket: "ticket_planter",
    festive: "festive_planter",
    sticker: "sticker_planter",
    plastic: "plastic_planter",
    candy: "candy_planter",
    red_clay: "red_clay_planter",
    blue_clay: "blue_clay_planter",
    tacky: "tacky_planter",
    pesticide: "pesticide_planter",
    'heat-treated': "heat-treated_planter",
    hydroponic: "hydroponic_planter",
    petal: "petal_planter",
    planter_of_plenty: "planter_of_plenty_planter"
}