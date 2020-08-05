/** Cache often used elements */
const $donutList = $("#donut-list");

/** Base URL currently set for home use. */
const BASE_URL = "http://localhost:5000/api"

/** Create and append form */
function addForm() {
  const form = $(`
  <div class="form-style">
    <form id="donut-form">
      <fieldset><legend>Add a Donut!</legend>
        <label for="flavor"><span>Flavor </span><input class="input-field" name="flavor" id="form-flavor" type="text"></label>
        <label for="size"><span>Size </span><select name="size" class="select-field" id="form-size" type="text">
          <option value="Large">Large</option>
          <option value="Medium">Medium</option>
          <option value="Small">Small</option>
          </select>
        </label>
        <label for="rating"><span>Rating </span><input class="input-field" name="rating" id="form-rating" min="0" max="10" type="number"></label>
        <label for="image"><span>Image </span><input class="input-field" name="image" id="form-image" type="url"></label>
        <label><span> </span><input type="submit" value="Add It!" id="donut-add"></label>
      </fieldset>
    </form>
  </div>
  `);

  $("#form-skeleton").replaceWith(form);
}

/** Generate donut html from data. */
function generateDonut(donut) {
  return $(`
    <div class="donut-card" data-donut-id="${donut.id}">
      <li>${donut.flavor} / ${donut.size} / ${donut.rating}</li>
      <img src="${donut.image}"
      alt="(A delicious donut!)"
      class="donut-img">
      <button class="donut-delete">Annihilate Donut</button>
    </div>
  `);
}

/** Display all donuts */
async function initialDonutDisplay() {
  let resp = await axios.get(`${BASE_URL}/donuts`);

  for (let donutData of resp.data.donuts) {
    $donutList.append(generateDonut(donutData));
  }
}

/** Submits form entry to API */
$("#form-container").on("click", "#donut-add", async function (evt) {
  evt.preventDefault();
  
  let flavor = $("#form-flavor").val();
  let size = $("#form-size").val();
  let rating = $("#form-rating").val();
  let image = $("#form-image").val();
  
  const newDonutResponse = await axios.post(`${BASE_URL}/donuts`, {
    flavor,
    size,
    rating,
    image,
  });

  let newDonut = $(generateDonut(newDonutResponse.data.donut));
  $donutList.append(newDonut);


  $("#donut-form").trigger("reset");
})

/** Deletes a donut */
$("#donut-container").on("click", ".donut-delete", async function (evt) {
  evt.preventDefault();

  let $donut = $(evt.target).closest("div");
  let donutId = $donut.attr("data-donut-id");

  const deleteResponse = await axios.delete(`${BASE_URL}/donuts/${donutId}`);
  $donut.remove();
  $("#donut-message").innerText(`${deleteResponse.data.message}`);
});

/** Searches for donuts */
$("#form-container").on("click", "#donut-search", async function (evt) {
  evt.preventDefault();

  let searchVal = $("#form-search").val();

  let searchResponse = await axios.get(`${BASE_URL}/donuts/search/${searchVal}`);


});

$(initialDonutDisplay);
$(addForm);
