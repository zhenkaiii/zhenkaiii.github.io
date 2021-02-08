<?php
function dw_minion_dynamic_widget_js() {
  global $wp_customize;
  if ( ! isset( $wp_customize ) ) {
    wp_enqueue_script( 'dynamic-widget-js', get_template_directory_uri() . '/inc/js/dynamic-widget.js', array('jquery','jquery-ui-datepicker','jquery-ui-sortable','jquery-ui-sortable', 'jquery-ui-draggable','jquery-ui-droppable','admin-widgets' ) );
  }
  wp_enqueue_style( 'dynamic-widget-style', get_template_directory_uri() . '/inc/css/dynamic-widget.css', array() );
}
add_action( 'admin_enqueue_scripts', 'dw_minion_dynamic_widget_js' );

/**
 * Dynamic Widget
 */
class dw_dynamic_Widget extends WP_Widget {
  function widget( $args, $instance ) {
    extract( $args, EXTR_SKIP );
    echo $before_widget;
    $this->dw_display_widgets_front($instance);
    echo $after_widget;
  }
  function update( $new_instance, $old_instance ) {
    $updated_instance = $new_instance;
    return $updated_instance;
  }
  function form( $instance ) {
    global $wp_registered_widgets;
    $instance = wp_parse_args( $instance, array( 
      'widgets'    =>  '',
      'title'     =>  ''
    ) );
    ?>
      <input type="hidden" class="widefat" name="<?php echo $this->get_field_name('widgets') ?>" id="<?php echo $this->get_field_id('widgets') ?>" value="<?php echo htmlentities( $instance['widgets'] ) ?>" >
      <input type="hidden" name="<?php echo $this->get_field_name('title') ?>" id="<?php echo $this->get_field_id('title') ?>" value="<?php echo $instance['title'] ?>" class="widefat">
      <div class="dw-widget-extends" data-setting="#<?php echo $this->get_field_id('widgets') ?>" >
        <p class="description"><?php _e('Drag & Drop Widgets Here','dw_minion') ?></p>
        <?php
          $widgets = explode(':dw-data:', $instance['widgets'] );
          if( !empty($widgets) && is_array($widgets) ){
            $number = 1;
            foreach ($widgets as $widget) {
              if( !empty( $widget ) ) {
                $url = rawurldecode($widget);
                parse_str($widget,$s);
                $this->dw_display_widgets($s, $number);
              }
              $number++;
            }
          }
        ?>
      </div>
    <?php
  }
  function dw_get_widgets( $id_base, $number ){
    global $wp_registered_widgets;
    $widget = false;
    foreach ($wp_registered_widgets as $key => $wdg) {
      if( strpos( $key, $id_base ) === 0 ) {
        if( isset($wp_registered_widgets[ $key ]['callback'][0]) && is_object($wp_registered_widgets[ $key ]['callback'][0]) ) {
          $classname = get_class( $wp_registered_widgets[ $key ]['callback'][0] );
          $widget = new $classname;
          $widget->id_base = $id_base;
          $widget->number = $number;
          break;
        }
      }
    }
    return $widget;
  }
  function dw_display_widgets($s, $number){
    $instance = !empty($s['widget-'.$s['id_base']]) ? array_shift( $s['widget-'.$s['id_base']] ) : array();
    $widget = $this->dw_get_widgets( $s['id_base'], $number );
  ?>  
    <?php if( $widget ) { ?>
    <div id="<?php echo esc_attr($s['widget-id']); ?>" class="widget">
      <div class="widget-top">
        <div class="widget-title-action">
          <a class="widget-action hide-if-no-js" href="#available-widgets"></a>
          <a class="widget-control-edit hide-if-js" href="<?php echo esc_url( add_query_arg( $query_arg ) ); ?>">
            <span class="edit"><?php _ex( 'Edit', 'widget' ); ?></span>
            <span class="add"><?php _ex( 'Add', 'widget' ); ?></span>
            <span class="screen-reader-text"><?php echo $widget->name; ?></span>
          </a>
        </div>
        <div class="widget-title"><h4><?php echo $widget->name; ?><span class="in-widget-title"></span></h4></div>
      </div>
      <div class="widget-inside">
        <div class="widget-content">
          <?php if( isset($s['id_base'] ) ) { 
            $widget->form($instance); 
          } else { 
            echo "\t\t<p>" . __('There are no options for this widget.','dw_minion') . "</p>\n"; 
          } ?>
        </div>
        <input data-dw="true" type="hidden" name="widget-id" class="widget-id" value="<?php echo esc_attr($s['widget-id']); ?>" />
        <input data-dw="true" type="hidden" name="id_base" class="id_base" value="<?php echo esc_attr($s['id_base']); ?>" />
        <input data-dw="true" type="hidden" name="widget-width" class="widget-width" value="<?php echo esc_attr($s['widget-width']); ?>">
        <div class="widget-control-actions">
          <div class="alignleft">
            <a class="widget-control-remove" href="#remove"><?php _e('Delete','dw_minion'); ?></a> |
            <a class="widget-control-close" href="#close"><?php _e('Close','dw_minion'); ?></a>
          </div>
          <div class="alignright widget-control-noform">
            <?php submit_button( __( 'Save', 'dw_minion' ), 'button-primary widget-control-save right', 'savewidget', false, array( 'id' => 'widget-' . esc_attr( $s['widget-id'] ) . '-savewidget' ) ); ?>
            <span class="spinner"></span>
          </div>
          <br class="clear" />
        </div>
      </div>
      <div class="widget-description"><?php echo ( $widget_description = wp_widget_description($widget_id) ) ? "$widget_description\n" : "$widget_title\n"; ?></div>
    </div>
    <?php } ?>
  <?php
  }
}

/**
 * Tabs Widget
 */
class dw_tabs_Widget extends dw_dynamic_Widget {
  function dw_tabs_Widget() {
    $widget_ops = array( 'classname' => 'dw_tabs news-tab', 'description' => __('Display widgets inside a tab','dw_minion') );
    $this->WP_Widget( 'dw_tabs', 'DW: Tabs', $widget_ops );
  }
  function dw_display_widgets_front($instance){
    global $wp_registered_widget_updates;
    wp_parse_args($instance, array(
      'widgets' => array()
    ));
    $widgets = explode(':dw-data:', $instance['widgets'] );
    if( !empty($widgets) && is_array($widgets) ){ ?>
      <div class="nav-tab-select-wrap">
        <select name="nav-tabs-<?php echo $this->id ?>" class="nav-tabs-by-select visible-phone" >
          <?php
            $i = 0;
            foreach ($widgets as $widget ) {
              $selected = '';
              if( $i == 0 ){ $active='selected="selected"'; }
              $i++;
              if( !empty( $widget ) ) {
                $url = rawurldecode($widget);
                parse_str($url,$s);
                $instance = !empty($s['widget-'.$s['id_base']]) ? array_shift( $s['widget-'.$s['id_base']] ) : array();
                $widget = $this->dw_get_widgets( $s['id_base'], $i );
                if( $widget ) {
                  $widget_title = isset($instance['title']) ? $instance['title'] : $widget->name;
                  echo '<option data-target="#'.$s['widget-id'].'" '.$selected.' value="#'.$s['widget-id'].'" >'.strtoupper( $widget_title ).'</option>';
                }
              }
            }
          ?>
        </select>
      </div>
      <ul class="nav nav-tabs hidden-phone" id="nav-tabs-<?php echo $this->id ?>">
      <?php
      $i = 0;
      foreach ($widgets as $widget ) {
        $active = '';
        if( $i == 0 ){ $active='active'; } 
        $i++;
        if( !empty( $widget ) ) {
          $url = rawurldecode($widget);
          parse_str($widget,$s);
          $instance = !empty($s['widget-'.$s['id_base']]) ? array_shift( $s['widget-'.$s['id_base']] ) : array();
          $widget = $this->dw_get_widgets( $s['id_base'], $i );
          if( $widget ) {
            $widget_title = isset($instance['title']) ? $instance['title'] : $widget->name;
            echo '<li class="'.$active.'"><a href="#'.$s['widget-id'].'" data-toggle="tab">'.$widget_title.'</a></li>';
          }
        }
      }
      ?>
      </ul>
      <div class="tab-content">
        <?php
          $i=0;
          foreach ($widgets as $widget) {
            $active = '';
            if( $i == 0 ) { $active='active'; }
             $i++;
              if( !empty( $widget ) ) {
                $url = rawurldecode($widget);
                parse_str($widget,$s);
                $instance = isset($s['widget-'.$s['id_base']]) ? array_shift( $s['widget-'.$s['id_base']] ) : array();
                $widget = $this->dw_get_widgets( $s['id_base'], $i );
                if( isset($s['id_base'] ) && $widget ) {
                  $widget_options = $widget->widget_options; 
                ?>
                  <div class="tab-pane <?php echo 'widget_'.$s['widget-id'].' '.$widget_options['classname'] ?> <?php echo $active ?>" id="<?php echo $s['widget-id'] ?>">
                    <?php  
                      $default_args = array( 
                        'before_widget' => '', 
                        'after_widget' => '', 
                        'before_title' => '<h3 class="widget-title">',
                        'after_title' => '</h3>' 
                      );
                      $widget->widget($default_args,$instance);
                    ?>
                  </div>
                <?php
                }
              }
            }
          } 
        ?>
      </div>
  <?php
  }
}
add_action( 'widgets_init', create_function( '', "register_widget('dw_tabs_Widget');" ) );

/**
 * Accordion Widget
 */
class dw_accordion_Widget extends dw_dynamic_Widget {
  function dw_accordion_Widget() {
    $widget_ops = array( 'classname' => 'dw_accordion news-accordion', 'description' => __('Display widgets inside an accordion','dw_minion') );
    $this->WP_Widget( 'dw_accordions', 'DW: Accordion', $widget_ops );
  }
  function dw_display_widgets_front($instance){
    global $wp_registered_widget_updates;
    wp_parse_args($instance, array(
      'widgets' => array()
    ));
    $widgets = explode(':dw-data:', $instance['widgets'] );
    if( !empty($widgets) && is_array($widgets) ) {
      echo '<div class="accordion" id="accordion-'.$this->id.'">';
      $collapse = ''; $i = 0;
      foreach ($widgets as $widget) {
        $collapse = ( $i == 0 ) ? 'active' : 'collapsed';
        if( !empty( $widget ) ) {
          $url = rawurldecode($widget);
          parse_str($url,$s);
          $instance = !empty($s['widget-'.$s['id_base']]) ? array_shift( $s['widget-'.$s['id_base']] ) : array();
          $widget = $this->dw_get_widgets( $s['id_base'], $i );
          if( isset($s['id_base'] ) && $widget ){ ?>
            <?php $widget_options = $widget->widget_options; ?>
            <div class="accordion-group">
              <div class="accordion-heading"><a class="accordion-toggle <?php echo $collapse ?>" data-toggle="collapse" data-parent="#accordion-<?php echo $this->id ?>" href="#<?php echo $this->id ?>-<?php echo $s['widget-id'] ?>"><?php echo ( isset($instance['title']) ) ? $instance['title'] : $widget->name; ?></a></div>
              <div id="<?php echo $this->id ?>-<?php echo $s['widget-id'] ?>" class="<?php echo 'widget_'.$s['widget-id'].' ' ?> accordion-body collapse <?php echo $collapse == 'active' ? 'in' : ''; ?> <?php echo $widget_options['classname'] ?>">
                <div class="accordion-inner">
                <?php  
                $default_args = array( 
                    'before_widget' => '', 
                    'after_widget' => '', 
                    'before_title' => '<h3 class="widget-title">', 
                    'after_title' => '</h3>' 
                );
                $widget->widget($default_args,$instance);
                ?>
                </div>
              </div>
            </div>
          <?php
          }
        }
        $i++;
      }
      echo '</div>';
    }
  }
}
add_action( 'widgets_init', create_function( '', "register_widget('dw_accordion_Widget');" ) );

/**
 * DW Minion Navigation Menu Widget
 * This is Custom Menu in for Top Sidebar
 */
class DW_Minion_Navigation_Menu_Widget extends WP_Widget {

	public function __construct() {
		$widget_ops = array(
			'description' => __( 'Add a navigation menu to your Top Sidebar.' ),
			'customize_selective_refresh' => true,
		);
		parent::__construct( 'dw_minion_nav_menu', __('DW Minion Navigation Menu'), $widget_ops );
	}

	public function widget( $args, $instance ) {
		// Get menu
		$nav_menu = ! empty( $instance['nav_menu'] ) ? wp_get_nav_menu_object( $instance['nav_menu'] ) : false;

		if ( !$nav_menu )
			return;

		echo $args['before_widget'];

		$nav_menu_args = array(
			'fallback_cb' => '',
			'menu'        => $nav_menu
		);

		wp_nav_menu( apply_filters( 'widget_dw_minion_nav_menu_args', $nav_menu_args, $nav_menu, $args, $instance ) );

		echo $args['after_widget'];
	}

	/**
	 * Handles updating settings for the current Custom Menu widget instance.
	 *
	 * @since 3.0.0
	 * @access public
	 *
	 * @param array $new_instance New settings for this instance as input by the user via
	 *                            WP_Widget::form().
	 * @param array $old_instance Old settings for this instance.
	 * @return array Updated settings to save.
	 */
	public function update( $new_instance, $old_instance ) {
		$instance = array();
		if ( ! empty( $new_instance['nav_menu'] ) ) {
			$instance['nav_menu'] = (int) $new_instance['nav_menu'];
		}
		return $instance;
	}

	/**
	 * Outputs the settings form for the Custom Menu widget.
	 *
	 * @since 3.0.0
	 * @access public
	 *
	 * @param array $instance Current settings.
	 * @global WP_Customize_Manager $wp_customize
	 */
	public function form( $instance ) {
		global $wp_customize;
		$nav_menu = isset( $instance['nav_menu'] ) ? $instance['nav_menu'] : '';

		// Get menus
		$menus = wp_get_nav_menus();

		// If no menus exists, direct the user to go and create some.
		?>
		<p class="nav-menu-widget-no-menus-message" <?php if ( ! empty( $menus ) ) { echo ' style="display:none" '; } ?>>
			<?php
			if ( $wp_customize instanceof WP_Customize_Manager ) {
				$url = 'javascript: wp.customize.panel( "nav_menus" ).focus();';
			} else {
				$url = admin_url( 'nav-menus.php' );
			}
			?>
			<?php echo sprintf( __( 'No menus have been created yet. <a href="%s">Create some</a>.' ), esc_attr( $url ) ); ?>
		</p>
		<div class="nav-menu-widget-form-controls" <?php if ( empty( $menus ) ) { echo ' style="display:none" '; } ?>>
			<p>
				<label for="<?php echo $this->get_field_id( 'nav_menu' ); ?>"><?php _e( 'Select Menu:' ); ?></label>
				<select id="<?php echo $this->get_field_id( 'nav_menu' ); ?>" name="<?php echo $this->get_field_name( 'nav_menu' ); ?>">
					<option value="0"><?php _e( '&mdash; Select &mdash;' ); ?></option>
					<?php foreach ( $menus as $menu ) : ?>
						<option value="<?php echo esc_attr( $menu->term_id ); ?>" <?php selected( $nav_menu, $menu->term_id ); ?>>
							<?php echo esc_html( $menu->name ); ?>
						</option>
					<?php endforeach; ?>
				</select>
			</p>
			<?php if ( $wp_customize instanceof WP_Customize_Manager ) : ?>
				<p class="edit-selected-nav-menu" style="<?php if ( ! $nav_menu ) { echo 'display: none;'; } ?>">
					<button type="button" class="button"><?php _e( 'Edit Menu' ) ?></button>
				</p>
			<?php endif; ?>
		</div>
		<?php
	}
}

add_action( 'widgets_init', create_function( '', "register_widget('DW_Minion_Navigation_Menu_Widget');" ) );