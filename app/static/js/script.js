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
    var num = container.children.length; // Number of milestones currently
    var newMilestone = `
        <div class="form-group milestone-item" draggable="true" ondragstart="dragStart(event)" ondragover="dragOver(event)" ondrop="drop(event)">
            <input type="hidden" name="milestones-${num}-order" class="form-control milestone-order">
            <label for="milestones-${num}-title">Milestone Title</label>
            <input type="text" name="milestones-${num}-title" id="milestones-${num}-title" class="form-control" required>
            <div class="form-group">
                <label for="milestones-${num}-content">Content</label>
                <textarea name="milestones-${num}-content" id="milestones-${num}-content" class="form-control" rows="5" required></textarea>
            </div>
            <div class="form-group">
                <label for="milestones-${num}-image">Image</label>
                <input type="file" name="milestones-${num}-image" id="milestones-${num}-image" class="form-control-file">
            </div>
        </div>`;
    container.insertAdjacentHTML('beforeend', newMilestone);
    updateOrder();
}

function updateOrder() {
    var orderInputs = document.querySelectorAll('.milestone-order');
    orderInputs.forEach((input, index) => {
        input.value = index + 1;
    });
}

function dragStart(event) {
    event.dataTransfer.setData("text/plain", event.target.id);
    event.target.classList.add('dragging');
}

function dragOver(event) {
    event.preventDefault();
    event.target.classList.add('drag-over');
}

function drop(event) {
    event.preventDefault();
    event.target.classList.remove('drag-over');
    const id = event.dataTransfer.getData("text/plain");
    const draggableElement = document.getElementById(id);
    const dropzone = event.target.closest('.milestone-item');
    if (dropzone && dropzone !== draggableElement) {
        const container = document.getElementById('milestones');
        const siblings = Array.from(container.children);
        const dragIndex = siblings.indexOf(draggableElement);
        const dropIndex = siblings.indexOf(dropzone);

        if (dragIndex < dropIndex) {
            container.insertBefore(draggableElement, dropzone.nextSibling);
        } else {
            container.insertBefore(draggableElement, dropzone);
        }
        updateOrder();
    }
}

document.getElementById('milestones').addEventListener('dragend', (e) => {
    e.target.classList.remove('dragging');
    updateOrder();
});

document.getElementById('milestones').addEventListener('dragstart', (e) => {
    e.target.classList.add('dragging');
});

document.getElementById('milestones').addEventListener('dragover', (e) => {
    e.preventDefault();
    const afterElement = getDragAfterElement(e.clientY);
    const draggingElement = document.querySelector('.dragging');
    if (afterElement == null) {
        document.getElementById('milestones').appendChild(draggingElement);
    } else {
        document.getElementById('milestones').insertBefore(draggingElement, afterElement);
    }
});

function getDragAfterElement(y) {
    const draggableElements = [...document.querySelectorAll('.milestone-item:not(.dragging)')];
    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

function openModal(imageSrc) {
    var modal = document.getElementById("myModal");
    var modalImage = document.getElementById("modalImage");
    modal.style.display = "block";
    modalImage.src = imageSrc;
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}
