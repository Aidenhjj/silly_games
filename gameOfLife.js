//This is a GameOfLife implementation in JS

function Grid(n) {
  // Main game 'object'
  this.grid = [];
  for (var i = 0; i < n; i++) {
    this.grid.push([]);
    for (var j = 0; j < n; j++) {
      this.grid[i].push(Math.floor(Math.random() + 0.5));
    }
  }
}

Grid.prototype.get = function(x, y) {
  // gets number at (x,y)
  return this.grid[y][x];
};

Grid.prototype.neighbours = function(x, y) {
  // returns number of live neighbours
  var count = 0;
  for (var i = -1; i <= 1; i++) {
    for (var j = -1; j <= 1; j++) {
      var val = this.get(x + i, y + j);
      if ((val != undefined) && (val == 1) && !((i == 0) && (j == 0)))
        count++;
    }
  }
  return count;
};

Grid.prototype.show = function() {
  // returns game representation
  console.log(this.grid);
};

Grid.prototype.turn = function() {
  // runs one turn of game
  var temp = this.grid.slice();
  
  for (var i = 0; i < this.grid.length; i++) {
    for (var j = 0; j < this.grid.length; j++) {
      var n = this.neighbours(i, j);
      if (this.get(i, j) == 1)//alive
      {
        if (!((n >= 2) && (n <= 3)))
          temp[j][i] = 0;
      }
      else if (this.get(i, j) == 0)//dead
      {
        if (n == 3)
          temp[j][i] = 1;
      }
    }
  }
  
  this.grid = temp.slice();
};

var board = new Grid(10);
board.show();
board.turn();
board.show();