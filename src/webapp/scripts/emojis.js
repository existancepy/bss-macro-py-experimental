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