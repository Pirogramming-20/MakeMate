
function updateDropdowns() {

    const vote1 = document.getElementById("idea_vote1").value;
    const vote2 = document.getElementById("idea_vote2").value;
    const vote3 = document.getElementById("idea_vote3").value;
  
    document.querySelectorAll('select').forEach(function(select) {
      let isOptionSelected = select.value !== "" && select.value !== "아이디어 선택";
  
      Array.from(select.options).forEach(function(option) {
        if (option.value === "") {
          option.style.display = isOptionSelected ? "block" : "none";
        } else if (option.value !== "아이디어 선택") {
          if (option.value === vote1 || option.value === vote2 || option.value === vote3) {
            if (select.value !== option.value) {
              option.style.display = "none";
            }
          } else {
            option.style.display = "block";
          }
        }
      });
  
      if (!isOptionSelected) {
        select.selectedIndex = 0;
      }
    });
  }
  
  window.onload = updateDropdowns;
  