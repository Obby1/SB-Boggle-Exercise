class BoggleGame {
    /* make a new game at this DOM id */
  
    constructor(boardId, secs = 60) {
      this.secs = secs; // game length
      this.showTimer();
  
      this.score = 0;
      this.words = new Set();
      this.board = $("#" + boardId);
  
      // every 1000 msec, "tick"
      this.timer = setInterval(this.tick.bind(this), 1000);
  
      $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }
  
    /* show word in list of words */
  
    showWord(word) {
      $(".words", this.board).append($("<li>", { text: word }));
    }
  
    /* show score in html */
  
    showScore() {
      $(".score", this.board).text(this.score);
    }
  
    /* show a status message */
    // add cls to style with css later
    showMessage(msg, cls) {
      $(".msg", this.board)
        .text(msg)
        .removeClass()
        .addClass(`msg ${cls}`);
    }
  
    /* handle submission of word: if unique and valid, score & show */
  
    async handleSubmit(evt) {
      evt.preventDefault();
      const $word = $(".word", this.board);
  
      let word = $word.val();
      if (!word) return;
  
      if (this.words.has(word)) {
        this.showMessage(`Already found ${word}`, "err");
        return;
      }
  
      // check server for validity
        //    Ask krunal to help explain format to you
      const resp = await axios.get("/check-word", { params: { word: word }});
      if (resp.data.result === "not-word") {
        this.showMessage(`${word} is not a valid English word`, "err");
      } else if (resp.data.result === "not-on-board") {
        this.showMessage(`${word} is not a valid word on this board`, "err");
      } else {
        this.showWord(word);
        this.score += word.length;
        this.showScore();
        this.words.add(word);
        this.showMessage(`Added: ${word}`, "ok");
      }
  
      $word.val("").focus();
    }
  
    /* Update timer in DOM */
  
    showTimer() {
      $(".timer", this.board).text(this.secs);
    }
  
    /* Tick: handle a second passing in game */
  
    async tick() {
      this.secs -= 1;
      this.showTimer();
  
      if (this.secs === 0) {
        clearInterval(this.timer);
        await this.scoreGame();
      }
    }
  
    /* end of game: score and update message. */
    // krunal - why does every score follow {something:something} format? standard for axios?
    // add play again button after showing score
    async scoreGame() {
      $(".add-word", this.board).hide();
      const resp = await axios.post("/post-score", { score: this.score });
      if (resp.data.brokeRecord) {
        this.showMessage(`New record: ${this.score}`, "ok");
      } else {
        this.showMessage(`Final score: ${this.score}`, "ok");
      }
    }
  }

// // submit guess to server without refreshing page

// //declare vars
// let $guess = $('.guessForm')
// let $guessText = $('#guessText')
// let $currentGuess = ''

// $guess.on("submit", handleSubmit);


// function showMessage(msg, cls) {
//     $(".msg")
//       .text(msg)
//       .removeClass()
//       .addClass(`msg ${cls}`);
//   }


// async function handleSubmit(evt){
//     evt.preventDefault();

//     const $word = $(".guessText");    
//     let word = $word.val();
//     if (!word) return;  
//     console.log('working up to here')
//     // below is what's broken 
//     // let resp = await axios.get("/check-word", { params: { word: word }});    
//     const resp = await axios.get("/check-word", { params: { word: word }});
//     console.log('working down here')
//     if (resp.data.result === "not-word") {
//         showMessage(`${word} is not a valid English word`, "err");
//       } else if (resp.data.result === "not-on-board") {
//         showMessage(`${word} is not a valid word on this board`, "err");
//       } else {
//        showWord(word);
//         // this.score += word.length;
//         // this.showScore();
//         // words.add(word);
//         showMessage(`Added: ${word}`, "ok");
//       }
  
//       $word.val("").focus();
// }

// // const response = await axios({
// //     // url: ``,
// //     
// //     url: 'http://127.0.0.1:5000/guess',
// //     method: "POST",
// //   });

// // $guess.on("submit", async function (evt){
// //     evt.preventDefault();
// //     currentGuess = $guessText.val();
// //     console.log(currentGuess);
// //     $guessText.val('');
// //     const resp = await axios.get("/check-word", { params: { word: word }});
// //     return response
// //     // add flash showing submitted 
// // })

// // $guess.on("submit", async function (evt){
// //     evt.preventDefault();
// //     $currentGuess = $guessText.val();
// //     let word = $currentGuess;
// //     console.log(word);
// //     $guessText.val('');
// //     console.log('working up to here-----')
// //     const resp = await axios.get("/check-word", { params: { word: word }});
// //     if (resp.data.result === "not-word") {
// //         showMessage(`${word} is not a valid English word`, "err");
// //       } else if (resp.data.result === "not-on-board") {
// //         showMessage(`${word} is not a valid word on this board`, "err");
// //       } else {
// //         showWord(word);
// //         // score += word.length;
// //         // showScore();
// //         // words.add(word);
// //         showMessage(`Added: ${word}`, "ok");
// //       }
// //     // add flash showing submitted 
// // })
