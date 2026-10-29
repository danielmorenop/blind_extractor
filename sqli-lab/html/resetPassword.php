<?php
$host = getenv('DB_HOST');
$user = getenv('DB_USER');
$pass = getenv('DB_PASS');
$db = getenv('DB_NAME');

$conn = new mysqli($host, $user, $pass, $db);

$message = "";
$is_success = false;

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'] ?? '';

    // ==========================================
    // QUERY VULNERABLE TO BOOLEAN BLIND SQLi
    // ==========================================
    // Injection in the email field. There is no validation or use of prepared statements.
    $query = "SELECT * FROM users WHERE email = '" . $email . "'";
    
    $result = $conn->query($query);

    // ==========================================
    // BOOLEAN BEHAVIOR (TRUE / FALSE)
    // ==========================================
    if ($result && $result->num_rows > 0) {
        // TRUE: The query is valid and returns at least one record.
        $message = "A password reset link has been sent to your email address.";
        $is_success = true;
    } else {
        // FALSE: The query is invalid or returns no results.
        $message = "The entered email address does not exist in our system.";
        $is_success = false;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Reset Password - Boolean Lab</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 320px; }
        h2 { text-align: center; color: #333; font-size: 20px; }
        p.desc { text-align: center; color: #666; font-size: 13px; margin-bottom: 20px;}
        .input-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; color: #666; font-size: 14px;}
        input[type="email"], input[type="text"] { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { width: 100%; background: #28a745; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #218838; }
        .message { margin-top: 15px; text-align: center; font-size: 14px; font-weight: bold; padding: 10px; border-radius: 4px; }
        .msg-success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .msg-error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>

<div class="login-card">
    <h2>Reset Password</h2>
    <p class="desc">Enter your email address and we will send you instructions.</p>
    
    <form method="POST" action="">
        <div class="input-group">
            <label>Email Address:</label>
            <!-- Note: In a real scenario this would be type="email", but we use type="text" so the browser doesn't block single quotes or payloads when testing manually from the web UI -->
            <input type="text" name="email" required placeholder="user@company.local">
        </div>
        <button type="submit">Send Link</button>
    </form>

    <?php if (!empty($message)): ?>
        <div class="message <?php echo $is_success ? 'msg-success' : 'msg-error'; ?>">
            <?php echo $message; ?>
        </div>
    <?php endif; ?>
</div>

</body>
</html>
