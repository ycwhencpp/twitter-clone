// button
const follow_btn = document.querySelector(".follow-button");

// follow / unfollow user
follow_btn.onclick = () => {
  const profile_username = follow_btn.dataset.username;
  console.log(profile_username);
  const follower_count = document.querySelector(".followers");
  const following_count = document.querySelector(".following");
  fetch("/editprofile", {
    method: "PUT",
    body: JSON.stringify({
      username: profile_username,
      following: true,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.error) console.log(data.error);
      else {
        console.log(data.message);
        follower_count.innerHTML = `followers:${data.followerscount}`;
        following_count.innerHTML = `following:${data.followingcount}`;
        follow_btn.innerHTML == "Follow" ? (follow_btn.innerHTML = "UnFollow") : (follow_btn.innerHTML = "Follow");
      }
    })
    .catch((error) => console.log(error));
};
