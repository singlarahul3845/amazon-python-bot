function save_post_url_to_pdp_prices($post_id, $post, $update) {
    // If this is a revision, don't update the table.
    if (wp_is_post_revision($post_id)) {
        return;
    }

    // Check if it's not an autosave.
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    // Check the post status
    if ('publish' !== $post->post_status) {
        return;
    }

    global $wpdb;
    $table_name = $wpdb->prefix . 'pdp_prices';

    // Prepare URL and default price
    $post_url = get_permalink($post_id);
    $default_price = 0.00;  // Define your default price logic here

    // Fetch the original post ID if this is a translated post
    $original_post_id = get_post_meta($post_id, '_translated_from_post_id', true);
    if (!$original_post_id) {
        $original_post_id = $post_id;
    }

    // Fetch the translated post URLs from the wp_translated_posts_id table
    $translated_posts_table = $wpdb->prefix . 'translated_posts_id';
    $translated_posts = $wpdb->get_row($wpdb->prepare("SELECT * FROM $translated_posts_table WHERE original_post_id = %d", $original_post_id), ARRAY_A);

    // Ensure $translated_posts is an array
    if (!$translated_posts) {
        $translated_posts = [];
    }

    // Prepare the data to be inserted/updated in wp_pdp_prices
    $data = [];
    if ($post_id == $original_post_id) {
        $data['original_post_url'] = $post_url;
    } else {
        $language = array_search($post_id, $translated_posts);
        $column_name = str_replace('_post_id', '_post_url', $language);
        $data[$column_name] = $post_url;
    }
    $data['prices'] = $default_price;

    // Add translated URLs
    if ($translated_posts) {
        foreach ($translated_posts as $language => $translated_post_id) {
            if ($translated_post_id && $translated_post_id != $post_id) {
                $translated_post_url = get_permalink($translated_post_id);
                $column_name = str_replace('_post_id', '_post_url', $language);
                $data[$column_name] = $translated_post_url;
            }
        }
    }

    // Check if the original post URL already exists in the table
    $existing_entry = $wpdb->get_row($wpdb->prepare("SELECT * FROM $table_name WHERE original_post_url = %s", get_permalink($original_post_id)));

    if ($existing_entry) {
        // Update the existing record
        $wpdb->update(
            $table_name,
            $data,
            array('original_post_url' => get_permalink($original_post_id))
        );
    } else {
        // Insert a new record
        $wpdb->insert(
            $table_name,
            $data
        );
    }

    // Fetch all URLs from the table
    $urls = $wpdb->get_results("SELECT * FROM $table_name", ARRAY_A);
    $all_urls = [];
    foreach ($urls as $row) {
        foreach ($row as $key => $value) {
            if (strpos($key, '_post_url') !== false && $value) {
                $all_urls[$key] = $value;
            }
        }
    }

    // Call function to attach categories
    attach_categories_to_posts($all_urls);

    // Return array of all URLs
    return $all_urls;
}

function attach_categories_to_posts($urls) {
    foreach ($urls as $key => $url) {
        $post_id = url_to_postid($url);
        if (strpos($key, 'original_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('English')));
        } elseif (strpos($key, 'hindi_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Hindi')));
        } elseif (strpos($key, 'bengali_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Bengali')));
        } elseif (strpos($key, 'telugu_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Telugu')));
        } elseif (strpos($key, 'marathi_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Marathi')));
        } elseif (strpos($key, 'tamil_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Tamil')));
        } elseif (strpos($key, 'urdu_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Urdu')));
        } elseif (strpos($key, 'gujarati_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Gujarati')));
        } elseif (strpos($key, 'kannada_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Kannada')));
        } elseif (strpos($key, 'malayalam_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Malayalam')));
        } elseif (strpos($key, 'punjabi_post_url') !== false) {
            wp_set_post_categories($post_id, array(get_cat_ID('Punjabi')));
        }
    }
}

// Hook into the save_post action
add_action('save_post', 'save_post_url_to_pdp_prices', 10, 3);