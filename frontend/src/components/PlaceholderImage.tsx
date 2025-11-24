import React from 'react';
import { View, StyleSheet } from 'react-native';
import Svg, { Rect, Circle, Path, Text as SvgText, G } from 'react-native-svg';
import { darkTheme } from '../theme';

interface PlaceholderImageProps {
  contentType: string;
  width?: number;
  height?: number;
}

const PlaceholderImage: React.FC<PlaceholderImageProps> = ({ 
  contentType, 
  width = 400, 
  height = 225 
}) => {
  const getColorScheme = (type: string) => {
    const scheme = darkTheme.placeholders[type as keyof typeof darkTheme.placeholders];
    return scheme || darkTheme.placeholders.article;
  };

  const colors = getColorScheme(contentType);

  const renderIcon = () => {
    switch (contentType) {
      case 'paper':
        return (
          <G>
            <Rect x="170" y="80" width="60" height="80" fill={colors.accent} rx="2" />
            <Rect x="175" y="90" width="50" height="3" fill="white" opacity="0.8" />
            <Rect x="175" y="100" width="45" height="3" fill="white" opacity="0.8" />
            <Rect x="175" y="110" width="50" height="3" fill="white" opacity="0.8" />
            <Rect x="175" y="120" width="40" height="3" fill="white" opacity="0.8" />
            <Rect x="175" y="135" width="35" height="15" fill={colors.icon} rx="1" />
          </G>
        );
      
      case 'research':
        return (
          <G>
            <Circle cx="200" cy="112" r="35" fill={colors.accent} opacity="0.2" />
            <Circle cx="200" cy="112" r="25" fill={colors.accent} opacity="0.4" />
            <Circle cx="200" cy="112" r="15" fill={colors.accent} />
            <Path d="M 185 97 L 215 97 M 200 82 L 200 142" stroke={colors.icon} strokeWidth="3" />
          </G>
        );
      
      case 'news':
        return (
          <G>
            <Rect x="165" y="85" width="70" height="55" fill={colors.accent} rx="3" />
            <Rect x="172" y="95" width="56" height="4" fill="white" opacity="0.9" />
            <Rect x="172" y="105" width="50" height="3" fill="white" opacity="0.7" />
            <Rect x="172" y="112" width="45" height="3" fill="white" opacity="0.7" />
            <Rect x="172" y="119" width="40" height="3" fill="white" opacity="0.7" />
            <Circle cx="185" cy="130" r="4" fill={colors.icon} />
          </G>
        );
      
      case 'tutorial':
        return (
          <G>
            <Path 
              d="M 200 80 L 180 100 L 200 120 L 220 100 Z" 
              fill={colors.accent} 
              opacity="0.3"
            />
            <Path 
              d="M 200 90 L 185 105 L 200 120 L 215 105 Z" 
              fill={colors.accent}
            />
            <Rect x="195" y="125" width="10" height="20" fill={colors.icon} />
            <Path 
              d="M 185 145 L 200 135 L 215 145" 
              stroke={colors.icon} 
              strokeWidth="3" 
              fill="none"
            />
          </G>
        );
      
      case 'essay':
        return (
          <G>
            <Rect x="175" y="80" width="50" height="65" fill={colors.accent} rx="2" />
            <Path 
              d="M 180 90 Q 200 95 220 90" 
              stroke="white" 
              strokeWidth="2" 
              fill="none"
              opacity="0.8"
            />
            <Path 
              d="M 180 100 Q 200 105 220 100" 
              stroke="white" 
              strokeWidth="2" 
              fill="none"
              opacity="0.8"
            />
            <Path 
              d="M 180 110 Q 200 115 220 110" 
              stroke="white" 
              strokeWidth="2" 
              fill="none"
              opacity="0.8"
            />
            <Path 
              d="M 180 120 Q 200 125 220 120" 
              stroke="white" 
              strokeWidth="2" 
              fill="none"
              opacity="0.8"
            />
          </G>
        );
      
      case 'post':
        return (
          <G>
            <Circle cx="200" cy="105" r="30" fill={colors.accent} opacity="0.3" />
            <Rect x="180" y="95" width="40" height="4" fill={colors.accent} rx="2" />
            <Rect x="185" y="105" width="30" height="3" fill={colors.accent} rx="1" />
            <Rect x="187" y="113" width="26" height="3" fill={colors.accent} rx="1" />
            <Path 
              d="M 195 125 L 200 135 L 205 125" 
              stroke={colors.icon} 
              strokeWidth="3" 
              fill="none"
            />
          </G>
        );
      
      case 'article':
      default:
        return (
          <G>
            <Rect x="170" y="85" width="60" height="55" fill={colors.accent} rx="2" />
            <Rect x="177" y="95" width="46" height="5" fill="white" opacity="0.9" />
            <Rect x="177" y="105" width="40" height="3" fill="white" opacity="0.7" />
            <Rect x="177" y="112" width="43" height="3" fill="white" opacity="0.7" />
            <Rect x="177" y="119" width="38" height="3" fill="white" opacity="0.7" />
            <Rect x="177" y="126" width="35" height="3" fill="white" opacity="0.7" />
          </G>
        );
    }
  };

  return (
    <View style={[styles.container, { width, height }]}>
      <Svg width={width} height={height} viewBox="0 0 400 225">
        <Rect width="400" height="225" fill={colors.bg} />
        {renderIcon()}
      </Svg>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: darkTheme.background.tertiary,
  },
});

export default PlaceholderImage;

