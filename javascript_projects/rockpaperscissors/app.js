const computerChoiceDisplay = document.getElementById('computer-choice') // corresponds to span id 'computer-choice' from index.html
const playerChoiceDisplay = document.getElementById('player-choice') // corresponds to span id 'player-choice' from index.html
const resultDisplay = document.getElementById('result') // corresponds to span id 'result' from index.html
const possibleChoices = document.querySelectorAll('button')  //corresponds to buttons in index.html


let playerChoice
let computerChoice
let result
// establish 3 variables to store one value for each section of game: 1. player input, 2. computer's input from random num generator, 3. result
// function runs ---> function's result is stored within variable 

possibleChoices.forEach(possibleChoice => possibleChoice.addEventListener('click', (e) => {
    playerChoice = e.target.id
    playerChoiceDisplay.innerHTML = playerChoice
    generateComputerChoice()
    getResult()
    // section takes user player/user input from button clicks/presses
    // game has 3 sections where info is displayed
    // because there is only 1 player, the computer's input is determined by the player's input
    // computer input determined by its own random number generator function: generateComputerChoice()
    // player and result both handled by 1 function: getResult()
    
}))

function generateComputerChoice() {
    const randomNumber = Math.floor(Math.random() * 3) + 1 // or you can use possibleChoices.length, will return: 3
    console.log(randomNumber)
        //Math.random() generates a decimal number from 0(inclusive) to 0.99(inclusive)
        //multiply the random generated decimal by 3 to produce a random number between 0(inclusive) and 3(inclusive)
        //number used to multiply with the random decimal (in this case 3) is the maximum number that can be generated
        //use Math.floor to round down to nearest whole number, limits possible results to (0, 1, 2, 3)
        //add 1 to the solution to Math.floor() function to exclude 0 from possible results/make 1 the minimum possible value, possible values: (1, 2, 3)
    
    if (randomNumber === 1) {
    computerChoice = 'rock'
    }
    if (randomNumber === 2) {
    computerChoice = 'paper'
    }
    if (randomNumber === 3) {
    computerChoice = 'scissors'
    }
    computerChoiceDisplay.innerHTML = computerChoice // corresponds to 'click' eventListener above^^
    // .innerHTML calls back to/corresponds to/links to HTML display within index.html file
    // no result displays on webpage without .innerHTML call back
}

function getResult() {
    if (computerChoice === playerChoice) {
        result = 'its a draw!'
    }
    if (computerChoice === 'rock' && playerChoice === 'paper') {
        result = 'you win!'
    }
    if (computerChoice === 'rock' && playerChoice === 'scissors') {
        result = 'you lose!'
    }
    if (computerChoice === 'paper' && playerChoice === 'rock') {
        result = 'you lose!'
    }
    if (computerChoice === 'paper' && playerChoice === 'scissors') {
        result = 'you win!'
    }
    if (computerChoice === 'scissors' && playerChoice === 'paper') {
        result = 'you lose!'
    }
    if (computerChoice === 'scissors' && playerChoice === 'rock') {
        result = 'you win!'
    }
    resultDisplay.innerHTML = result // corresponds to 'click' eventListener above^^
    // .innerHTML calls back to/corresponds to/links to HTML display within index.html file
    // no result displays on webpage without .innerHTML call back
}