let games = null;
let selectedGameId = null;
let selectedGameData = null;
let categories = null;
let title = null;
let sport = "basketball";

const defaultUrl =
  "https://docs.google.com/spreadsheets/d/1lePLaeywOD97irRoD7qWcE3GHFMYimTPX1g77Vj-Yz8/edit?usp=sharing";
const statifyUrl = "http://127.0.0.1:5000";
const DUMMY_PRODUCTS = [
  {
    name: "Sheety",
    shortDescription: "Turn any Google Sheet into an API",
    website: "https://www.sheety.co",
    votes: 100,
    iconUrl: "https://sheety.co/icon.png",
    category: "Web",
    id: 2,
  },
];
const CATEGORIES = [
  {
    name: "Box Score",
    recordType: "box_score",
    id: 1,
  },
  {
    name: "Play-by-Play",
    recordType: "pbp",
    id: 2,
  },
  {
    name: "Team Stats",
    recordType: "team_stats",
    id: 3,
  },
];

const CATEGORY_HEADINGS = {
  games: [
    "Game #",
    "Date Played",
    "Team 1",
    "Team 2",
    "Team 1 Score",
    "Team 2 Score",
  ],
  box_score: [
    "PLAYER",
    "MIN",
    "FG",
    "3PT",
    "FT",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TO",
    "PF",
    "PTS",
  ],
  pbp: ["QUARTER", "TIME", "TEAM", "PLAY", "SCORE"],
  team_stats: [
    "PTS",
    "FG",
    "Field Goal %",
    "3PT",
    "Three Point %",
    "FT",
    "Free Throw %",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TO",
    "PF",
  ],
};

const CATEGORY_ALIGNMENT = {
  games: "center",
  box_score: "right",
  pbp: "left",
};

// Called once the page has loaded
document.addEventListener("DOMContentLoaded", function (event) {
  loadGames();
  loadCategories();
});

function loadGames() {
  selectedGameId = null;
  loadCategories();
  fetch(statifyUrl + "/api/basketball/game/all")
    .then((response) => response.json())
    .then((data) => {
      const { records } = data["games"];
      showAllGames(records);
    })
    .catch((err) => {
      showAllGames();
      return;
    });
}

function loadCategories() {
  this.categories = selectedGameId ? CATEGORIES : [];
  drawCategories();
}

function drawRecords(recordsList, record_type) {
  headings = CATEGORY_HEADINGS[record_type];
  recordsList = recordsList.map((recordsListObj) => {
    recordsListObj.headings = headings;
    return recordsListObj;
  });
  const template = Handlebars.compile(
    document.getElementById("records-template").innerHTML
  );
  const foundRecords = !recordsList[0].records;
  document.getElementById("records-container").innerHTML = template({
    title: this.title,
    headings: headings,
    recordsList: recordsList,
    foundRecords: foundRecords,
    errorMessage: "No records found",
  });
}

function drawCategories() {
  const template = Handlebars.compile(
    document.getElementById("menu-template").innerHTML
  );
  document.getElementById("menu-container").innerHTML = template(
    this.categories
  );
}

function showAllGames(records) {
  records_list = new Array();
  records_list_obj = {
    listLabel: "All Games",
    records: records,
    isGames: true,
    align: CATEGORY_ALIGNMENT["games"],
  };
  records_list.push(records_list_obj);
  drawRecords(records_list, "games");
}

function showCategory(category, recordType) {
  this.title = category;
  player_stat_records = [];
  for (const [key, values] of Object.entries(selectGameData[recordType])) {
    if (key !== "headings") {
      records_list_obj = {
        listLabel: selectGameData["teams"].includes(key) ? key : null,
        records: values,
        align: CATEGORY_ALIGNMENT[recordType],
      };
      player_stat_records.push(records_list_obj);
    }
  }
  drawRecords(player_stat_records, recordType);
}

function selectGame(gameId) {
  gameId = +gameId;
  getGame(gameId);
}

function getGame(gameId) {
  if (gameId === selectedGameId) return;

  fetch(statifyUrl + "/api/basketball/game/" + gameId)
    .then((response) => response.json())
    .then((data) => {
      selectGameData = data;
      selectedGameId = gameId;
      loadCategories();
      showCategory("Box Score", "box_score");
    })
    .catch((err) => {
      // location.reload();
      return;
    });
}

Handlebars.registerHelper("getId", function (values) {
  return values[0];
});

Handlebars.registerHelper("getNonIdValues", function (values) {
  return values.slice(1);
});
