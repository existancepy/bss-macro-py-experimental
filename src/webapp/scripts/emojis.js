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
    sticker_printer: "🖨️",
    stockings: "🧦",
    feast: "🍽️",
    samovar: "🏺",
    snow_machine: "❄️",
    lid_art: "🖼️",
    candles: "🕯️",
    wreath: "🎄",
    ant_challenge: "🎯",
    mondo_buff: "🐣",
    stinger_hunt: "😈",
}