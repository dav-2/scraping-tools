// Utility function to wait for an element to appear in the DOM
const waitForElement = (selector, timeout = 10000) => {
  return new Promise((resolve, reject) => {
    const interval = 100;
    let elapsed = 0;

    const check = setInterval(() => {
      const element = document.querySelector(selector);
      if (element) {
        clearInterval(check);
        resolve(element);
      } else if (elapsed >= timeout) {
        clearInterval(check);
        reject(`Element ${selector} not found within ${timeout}ms.`);
      }
      elapsed += interval;
    }, interval);
  });
};

// Utility function to extract usernames from a list
const extractUsernames = (elements) => {
  return Array.from(elements).map((item) => {
    const href = item.getAttribute('href');
    return href ? href.slice(1, -1) : null; // Remove leading/trailing slashes
  }).filter((username) => username); // Exclude null or invalid usernames
};

// Main function to get the users not following back
const findNotFollowingBack = async () => {
  try {
    // Open Followers list
    const followersButton = await waitForElement('a[href*="/followers/"]');
    followersButton.click();

    // Wait for the followers list to load
    await waitForElement('div[role="dialog"] div[role="button"] a[role="link"]');
    const followersList = document.querySelectorAll('div[role="dialog"] div[role="button"] a[role="link"]');
    const followersUsernames = extractUsernames(followersList);

    // Open Following list
    const followingButton = await waitForElement('a[href*="/following/"]');
    followingButton.click();

    // Wait for the following list to load
    await waitForElement('div[role="dialog"] div[role="button"] a[role="link"]');
    const followingList = document.querySelectorAll('div[role="dialog"] div[role="button"] a[role="link"]');
    const followingUsernames = extractUsernames(followingList);

    // Find users not following back
    const notFollowingBack = followingUsernames.filter((username) => !followersUsernames.includes(username));
    const distinctNotFollowingBack = [...new Set(notFollowingBack)];

    // Log the result
    console.log("Users who are not following back:");
    console.log(distinctNotFollowingBack);
  } catch (error) {
    console.error("Error:", error);
  }
};

// Execute the function
findNotFollowingBack();
