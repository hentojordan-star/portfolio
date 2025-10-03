// Broken / bulky JS for "before" version
// The functions attempt dynamic behavior but have subtle bugs and inefficiencies.

/* BUG: Wrong selector used in some places, causing functions to fail silently. */
/* ISSUE: Everything is in global scope and not modular. */

// Try to load more news when clicking "Load More News"
document.getElementById('loadNews').addEventListener('click', function() {
  // Simulated slow operation
  // BUG: Using setTimeout with heavy DOM writes causing perceived slowness
  setTimeout(function() {
    var container = document.getElementById('news-list'); // OK sometimes
    // ISSUE: Using innerHTML += with large strings can reflow a lot
    container.innerHTML += '<article class="news-item"><h3>New Lab Opened</h3><p>School science lab updated with new equipment.</p></article>';
    container.innerHTML += '<article class="news-item"><h3>Alumni Meet</h3><p>Alumni gathering scheduled for next month.</p></article>';
  }, 1200); // simulated delay
});

// Announcements show function - slightly wrong element targeting
// BUG: Using showAnn id may not always refer to correct element if nav structure changes
var showBtn = document.getElementById('showAnn');
if (showBtn) {
  showBtn.addEventListener('click', function() {
    var list = document.getElementById('announce-list');
    // ISSUE: toggling display directly without checking current state
    if (list.style.display === 'none') {
      list.style.display = 'block';
    } else {
      list.style.display = 'none';
    }
  });
}

// Submit announcement (does not persist - only temporary DOM update)
var form = document.getElementById('announceForm');
if (form) {
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var input = document.getElementById('announceInput');
    // BUG: No validation and direct DOM insert; also input not cleared sometimes
    if (input && input.value.trim() !== '') {
      var list = document.getElementById('announce-list');
      var item = document.createElement('div');
      item.className = 'announce-item';
      item.textContent = input.value; // ISSUE: no sanitization (XSS risk)
      list.appendChild(item);
      // BUG: input.value is not reliably cleared due to missing reference in some browsers
      input.value = '';
    }
  });
}

// Scores rendering - originally intended to build table dynamically
function renderScores() {
  // BUG: This function is never called anywhere (dead code)
  var scores = [
    { name: 'John Doe', math: 78, english: 88, science: 90 },
    { name: 'Jane Smith', math: 92, english: 85, science: 87 },
    { name: 'Mark Lee', math: 64, english: 73, science: 70 }
  ];
  var table = document.querySelector('.scores-table');
  if (!table) return;
  // ISSUE: Directly setting innerHTML may wipe table headers if used improperly
  var html = '<tr><th>Name<th>Math<th>English<th>Science';
  scores.forEach(function(s) {
    html += '<tr><td>' + s.name + '<td>' + s.math + '<td>' + s.english + '<td>' + s.science;
  });
  table.innerHTML = html; // BUG: replaces original structure unexpectedly
}

// Calendar highlight attempt - flawed Date usage
(function highlightToday() {
  // ISSUE: This logic assumes a particular date format in table cells; it fails silently
  var rows = document.querySelectorAll('.events-table tbody tr');
  var today = new Date().toDateString();
  for (var i = 0; i < rows.length; i++) {
    var cell = rows[i].querySelector('td');
    if (!cell) continue;
    // BUG: comparing full strings - will not match due to different formats
    if (cell.textContent.indexOf('Oct 1') !== -1 && today.indexOf('Oct') !== -1) {
      rows[i].style.background = '#eaf7ff'; // only triggers in specific conditions
    }
  }
})();

// Small helper - not used (leftover from attempted refactor)
function unusedHelper() {
  // ISSUE: dead code present, shows lack of cleanup
  return true;
        }
      
