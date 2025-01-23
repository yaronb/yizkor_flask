// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
}

function addMilestone() {
    var container = document.getElementById("milestones");
    var num = container.children.length / 3; // Number of milestones currently
    var newMilestone = `
        <div class="form-group">
            <label for="milestones-${num}-title">Milestone Title</label>
            <input type="text" name="milestones-${num}-title" id="milestones-${num}-title" class="form-control" required>
        </div>
        <div class="form-group">
            <label for="milestones-${num}-content">Content</label>
            <textarea name="milestones-${num}-content" id="milestones-${num}-content" class="form-control" rows="5" required></textarea>
        </div>
        <div class="form-group">
            <label for="milestones-${num}-image">Image</label>
            <input type="file" name="milestones-${num}-image" id="milestones-${num}-image" class="form-control-file">
        </div>`;
    container.insertAdjacentHTML('beforeend', newMilestone);
}