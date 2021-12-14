//elements
const like_form = document.querySelector("#like_form");
const retweet_form = document.querySelector("#retweet_form");
const edit_button = document.querySelectorAll(".edit_button");

// on click for each buttons
edit_button.forEach((button) => {
  button.onclick = () => {
    button.style.display = "none";
    const tweet_content = document.querySelector(`#tweet-content-${button.dataset.id}`);

    tweet_content.innerHTML = ` <form id="edit-form-${button.dataset.id}" data-id="${button.dataset.id}" class="edit-form" method="post" >
                      <textarea name="content" cols="40" rows="5" class="form-control content" 
                      id="tweet-content-edit" autofocus="on"  maxlength="1000" required="">${tweet_content.innerHTML}</textarea>
                      <input type="submit" class="btn btn-primary" value="Save" style="background:#00acee;
                       border: 1px solid #00acee;border-radius: 20px 20px;
                      padding:7px 20px;">
                      </form> `;

    document.querySelector(`#edit-form-${button.dataset.id}`).onsubmit = () => {
      const content = document.querySelector("#tweet-content-edit");
      fetch("/editpost", {
        method: "PUT",
        body: JSON.stringify({
          id: button.dataset.id,
          content: content.value,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            console.log(data.error);
          } else {
            console.log(data.message);
            tweet_content.innerHTML = content.value;
            button.style.display = "block";
          }
        })
        .catch((error) => console.log("error:", error));
      return false;
    };
  };
});

//like post

const like_button = document.querySelectorAll(".like-button");
like_button.forEach((button) => {
  button.onclick = () => {
    const id = button.dataset.id;
    const like_count = document.querySelector(`#like-post-${id}`);
    fetch("/editpost", {
      method: "PUT",
      body: JSON.stringify({
        id: id,
        liked: true,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) console.log(data.error);
        else {
          console.log(data.message);
          like_count.innerHTML = `${data.likes_count}`;
          if (button.innerHTML == '<i class="fas fa-heart" aria-hidden="true"></i>') {
            button.innerHTML = '<i class="far fa-heart" aria-hidden="true"></i>';
          } else {
            button.innerHTML = '<i class="fas fa-heart" aria-hidden="true"></i>';
          }
        }
      });
  };
});

// retweet  post
const rt_button = document.querySelectorAll(".rt-button");
rt_button.forEach((button) => {
  button.onclick = () => {
    console.log(button.innerHTML);
    const id = button.dataset.id;
    const rt_count = document.querySelector(`#rt-post-${id}`);
    fetch("/editpost", {
      method: "PUT",
      body: JSON.stringify({
        id: id,
        retweet: true,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) console.log(data.error);
        else {
          console.log(data.message);
          rt_count.innerHTML = `${data.retweetcount}`;
          if (button.innerHTML == '<i class="fas fa-retweet retweet-true" aria-hidden="true"></i>') {
            button.innerHTML = '<i class="fas fa-retweet" aria-hidden="true"></i>';
          } else {
            button.innerHTML = '<i class="fas fa-retweet retweet-true" aria-hidden="true"></i>';
          }
        }
      });
  };
});
